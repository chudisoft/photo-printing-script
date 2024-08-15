@echo off
cd /d "%~dp0"
call .\venv\Scripts\activate
python auto_photo_printer.py
pause
