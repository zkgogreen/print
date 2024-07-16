# print bridge project

## Installation

1. Download Python di [link ini](https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe), jangan lupa centang bagian ```add python to enviroment variable```
2. Download git di [link ini](https://git-scm.com/downloads),  jangan lupa pilih bagian ```use git from the window command promt```
3. jika sudah, buka terminal windows
4. ketik kode berikut ini di terminal
```bash
pip install virtualenv
```
```bash
mkdir project && cd project
```
```bash
virtualenv env && env\Scripts\activate.bat
```
```bash
pip install django reportlab pywin32
```
```bash
git clone https://github.com/zkgogreen/print.git
```
```bash
cd print && python manage.py runserver
```
5. Tunggu terminal hingga muncul link 127.0.0.1:8000
6. buka appsheet, dan mulai print
