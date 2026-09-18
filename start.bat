@echo off
cd /d "%~dp0"
set DATABASE_URL=sqlite:///fashion_store.db
call venv\Scripts\activate.bat
python app.py
