import json
import csv
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod

#common data interface
class DataAdapter(ABC): 
    def __init__(self,field_mapping = None, envelope = None):
        self.field_mapping = None  # Inicializa o field_mapping como None

    @abstractmethod
    def convert_to_json(self, file_path):
        pass

    def convert_file_to_json(self,file_path):
        return self.convert_to_json(file_path)
 
    def field_names_conversion(self, data):
        return data
 
    def strip_envelope(self, data):
        return data 
 
class CSVAdapter(DataAdapter):

    def __init__(self,field_mapping, envelope = None):
        self.field_mapping = field_mapping   
        self.envelope = envelope

    def convert_to_json(self, csv_file_path):
        data = []
        try:
            with open(csv_file_path, mode='r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file, delimiter='\t')
                for row in csv_reader:
                    row = self.field_names_conversion(row)
                    data.append(row)
        except FileNotFoundError:
            print(f"CSV file '{csv_file_path}' not found.")
        return json.dumps(data, indent=4)

    def field_names_conversion(self, row):  
        return {self.field_mapping.get(key, key): value for key, value in row.items()}
 
class XMLAdapter(DataAdapter):

    def __init__(self,field_mapping, envelope):
        self.envelope = envelope  
        self.field_mapping = field_mapping

    def convert_to_json(self, xml_file_path):

        def parse_element(element):
            parsed_data = {}
            if element:
                for child in element:
                    parsed_data[child.tag] =  parse_element(child) if list(child) else child.text
            else:
                parsed_data = element.text
            return [parsed_data] if parsed_data else None

        data = []
        try:
            tree = ET.parse(xml_file_path)
            root = tree.getroot()  
            data = parse_element(self.strip_envelope(root, self.envelope))  
        except FileNotFoundError:
            print(f"XML file '{xml_file_path}' not found.")
        return json.dumps(data, indent=4)
    
    def strip_envelope(self, element, envelope):
        for child in element:
            if child.tag == envelope:
                return child
            else:
                result = self.strip_envelope(child, envelope)
                if result is not None:
                    return result
        return None





def main():

    #complementary data to each transformation
    #csv transformation
    csv_field_mapping = {
            "Data Medicao": "data",
            "TEMPERATURA MAXIMA, DIARIA (AUT)(°C)": "temperatura_maxima",
            "TEMPERATURA MEDIA, DIARIA (AUT)(°C)": "temperatura_media",
            "TEMPERATURA MINIMA, DIARIA (AUT)(°C)": "temperatura_minima"
        }
    csv_adapter = CSVAdapter(csv_field_mapping)
    csv_json = csv_adapter.convert_file_to_json('data.csv')
    if csv_json:
        print("CSV to JSON:\n", csv_json)

    #xml transformation
    xml_envelope = "medicao"  
    xml_adapter = XMLAdapter(None,xml_envelope)  
    xml_json = xml_adapter.convert_file_to_json('data.xml')

    if xml_json:
        print("XML to JSON:\n", xml_json) 


    #join data in a single json
    combined_data = json.loads(csv_json or '[]') + json.loads(xml_json or '[]')
    combined_json = json.dumps(combined_data, indent=4)
    print("Combined JSON:\n", combined_json)

if __name__ == "__main__":
    main()