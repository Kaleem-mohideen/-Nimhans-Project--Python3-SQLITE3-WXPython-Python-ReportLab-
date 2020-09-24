#!env/bin/python
import os
from pathlib import Path
import datetime
import re

def createDir():
    _today = datetime.datetime.now()
    _year = _today.strftime("%Y")
    _month=_today.strftime("%b")
    _day=_today.strftime("%d")
    Path("Reports").mkdir(parents=True, exist_ok=True)
    Path("Reports/"+_year).mkdir(parents=True, exist_ok=True)
    Path("Reports/"+_year+"/" +_month).mkdir(parents=True, exist_ok=True)
    return "Reports/"+_year+"/" + _month 

def getFileName(_patientName, _mhr, _date=None):
    if _date == None:
        _date = datetime.date.today()
    if not isinstance(_date, datetime.date):
        raise TypeError('_date should be type datetime.date rceived {0} instead'.format(type(_date)))
    print(_date.strftime('%Y'))
    print(_date.strftime('%b'))
    _fileName= _patientName.replace(' ','') +  _mhr
    _directory = createDir()
    _pdfs = [_file for _file in os.listdir(_directory) if _file.startswith(_fileName) and _file.endswith('.pdf')]
    _extension = '0' + str(len(_pdfs)) if len(_pdfs) < 10 else str(len(_pdfs))
    return os.path.join(_directory,_fileName + _extension + '.pdf')

def getAge(_dob):
    if isinstance(_dob,datetime.date):
        pass
    else:
        raise TypeError('_dob is supposed be of type datetime.date received {0} instead'.format(type(_date)))
    _today = datetime.date.today()
    _diff = _today.year - _dob.year - ((_today.month, _today.day) < (_dob.month, _dob.day))
    return '{0} years'.format(_diff)



if __name__ == '__main__':
    print('works')
    createDir()
    print(getFileName('Vivek', '12345'))
