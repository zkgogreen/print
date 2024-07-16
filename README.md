# print bridge project

## Installation

1. install python [Python]("https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe")
2. buka terminal windows
3. ketik
```bash
pip install virtualenv
virtualenv env && cd env\Scripts\activate.bat
pip install django reportlab
git clone https://github.com/zkgogreen/print.git
cd print && python3 manage.py runserver
```
4. Tunggu terminal hingga muncul link 127.0.0.1:8000
5. buka appsheet, dan mulai print