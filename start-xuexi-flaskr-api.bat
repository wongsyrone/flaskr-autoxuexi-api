cd /d "%~dp0"

set FLASK_APP=flaskr.py
set PYTHONDONTWRITEBYTECODE=1

python -m flask run

:: use shell context to load/dump
::curl -L -O http://49.235.90.76:5000/api/questions
::ren questions data-input.json
::python -m flask shell

pause & break