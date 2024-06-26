@echo off
REM Check if virtualenv is installed
python -m pip show virtualenv >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    REM Install virtualenv if it's not installed
    echo Installing virtualenv...
    python -m pip install virtualenv
)

REM Create a virtual environment named 'env'
echo Creating virtual environment...
python -m virtualenv adapt_env

REM Activate the virtual environment
echo Activating virtual environment...
call adapt_env\Scripts\activate.bat

REM Inform the user that the virtual environment has been created and activated
echo Virtual environment 'env' has been created and activated.
pause