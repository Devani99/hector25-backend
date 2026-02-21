@echo off
echo ========================================
echo   Hector25 Backend - Starting Server
echo ========================================
echo.
echo Server will be available at:
echo   http://127.0.0.1:8000/
echo   http://127.0.0.1:8000/admin/
echo.
echo Press CTRL+C to stop.
echo.
venv\Scripts\python manage.py runserver
pause
