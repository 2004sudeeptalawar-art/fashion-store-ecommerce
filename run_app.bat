@echo off
cd /d "%~dp0"
call venv\Scripts\activate.bat
pip install Flask-SQLAlchemy Flask-Login Flask-WTF pymysql cryptography python-dotenv SQLAlchemy --quiet
python app.py
