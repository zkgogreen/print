@echo off

:: Navigate to the project directory
cd project

:: Activate the virtual environment
call env\Scripts\activate.bat

:: Navigate to the cloned repository
cd print

:: Pull repository
git pull

:: Run the Django makemigrations
python manage.py makemigrations

:: Run the Django migrate
python manage.py migrate

:: Run the Django server
python manage.py runserver

:: Keep the command prompt open
pause
