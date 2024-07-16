# print bridge project

## Installation

1. Download Python di [link ini](https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe)
2. jika sudah, buka terminal windows
3. ketik kode berikut ini di terminal
```bash
pip install virtualenv
```
```bash
mkdir project && cd project
```
```bash
virtualenv env && cd env\Scripts\activate.bat
```
```bash
pip install django reportlab
```
```bash
git clone https://github.com/zkgogreen/print.git
```
```bash
cd print && python3 manage.py runserver
```
4. Tunggu terminal hingga muncul link 127.0.0.1:8000
5. buka appsheet, dan mulai print
