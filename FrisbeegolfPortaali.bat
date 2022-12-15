@ECHO ON

pushd %~dp0

Set "VIRTUAL_ENV=dbenv"

IF NOT EXIST "%VIRTUAL_ENV%\Scripts\activate.bat" (
	pip.exe install virtualenv
    	python -m venv %VIRTUAL_ENV%
)

CALL proj_venv\Scripts\activate.bat
CALL python -m pip install --upgrade pip
CALL pip install -r requirements.txt
CALL python friba_ui.py
