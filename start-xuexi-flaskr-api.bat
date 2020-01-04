cd /d "%~dp0"

set FLASK_APP=flaskr.py
set PYTHONDONTWRITEBYTECODE=1

python -m flask run

pause & break