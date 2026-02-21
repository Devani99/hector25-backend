@echo off
echo ========================================
echo   Hector25 Backend - Setup Script
echo ========================================
echo.

echo [1/4] Creating virtual environment...
python -m venv venv
echo Done.

echo.
echo [2/4] Installing dependencies...
venv\Scripts\pip install -r requirements.txt
echo Done.

echo.
echo [3/4] Running database migrations...
venv\Scripts\python manage.py makemigrations accounts properties community notifications
venv\Scripts\python manage.py migrate
echo Done.

echo.
echo [4/4] Creating superuser (for Admin panel access)...
venv\Scripts\python manage.py createsuperuser

echo.
echo ========================================
echo   Setup Complete!
echo   Run: start.bat to start the server
echo ========================================
pause
