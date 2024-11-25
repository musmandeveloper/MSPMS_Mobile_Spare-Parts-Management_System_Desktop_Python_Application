


@echo off
::cd D:\Spare-Parts Management System - Python Thinker Project\My Working\Mobile Spare Parts Management System MSPMS

:: Fetching Project Folder Path dynamically either it is in Local Disk D, E or F etc
:: 01. %~dp0: This dynamically gets the path of the directory where the batch file is located, 
:: making the script work no matter where the project is stored.
:: 02. cd /d "%PROJECT_DIR%": Switches to the project directory, regardless of the drive or folder 
:: the project is in.

:: Get the current directory (location of this batch file)
set "PROJECT_DIR=%~dp0"

:: Navigate to the project directory
cd /d "%PROJECT_DIR%"

:: Actiavte Virtual Environment
call venv\Scripts\activate

:: Running Main File
python main.py

pause


