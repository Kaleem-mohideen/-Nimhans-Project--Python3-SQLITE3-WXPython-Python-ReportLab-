#!env/bin/python
import os
from pathlib import Path
import datetime

def createDir():
	_today = datetime.datetime.now()
	_year = _today.strftime("%Y")
	_month=_today.strftime("%b")
	_day=_today.strftime("%d")
	Path("Reports").mkdir(parents=True, exist_ok=True)
	Path("Reports/"+_year).mkdir(parents=True, exist_ok=True)
	Path("Reports/"+_year+"/" +_month).mkdir(parents=True, exist_ok=True)

if __name__ == '__main__':
    print('works')
    createDir()
