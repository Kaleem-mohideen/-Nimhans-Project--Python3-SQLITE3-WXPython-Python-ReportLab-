#!env/bin/python
import os
from pathlib import Path
import datetime
import re
import smtplib
import json
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import mimetypes
import base64





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



def sendEmail(_mailDict, _creds=None):
    '''
    _mailDict { key :
                {
                    'to': [_email...],
                    'cc': [_email....],
                    'bcc' = [_email...],
                    'body': _body,
                    'subject': _subject,
                    'attachments' : [list of attachments]
                }
              }
    _creds = {'from':_fromAddress, 'reply-to': if not the same as from address, 'login':, 'password':} - if none - reads from a file
    '''
    #IMPORTS HERE TO BE MOVED TO APPROPRIATE FILE
    if _creds == None:
        with open ('creds.json') as f:
            _creds = json.load(f)
    print (_creds)
    server =  smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    print(server.login(_creds['login'], _creds['auth']))
    print(_mailDict)
    for _key in _mailDict:
        print('_key: ', _key)
        if _mailDict[_key]['body'] == '':
            print("_mainDict[_key]['body']: ", _mainDict[_key]['body'])
            continue
        print('_key: ', _key)
        _senders =_mailDict[_key]['to']
        print('_senders: ', _senders)
        msg = MIMEMultipart()
        msg['From'] = _creds['login']
        if 'from' in _creds:
            msg['From'] = _creds['from']
        if 'reply-to' in _creds:
            msg['reply-to'] = _creds['reply-to']
        msg['To'] = ', '.join(_mailDict[_key]['to'])
        if 'cc' in _mailDict[_key]:
            _senders+= _mailDict[_key]['cc']
            msg['CC'] = ', '.join(_mailDict[_key]['cc'])
        if 'bcc' in _mailDict[_key]:
            _senders+= _mailDict[_key]['bcc']
        msg['Subject'] = _mailDict[_key]['subject']
        msg.attach(MIMEText(_mailDict[_key]['body'],'html'))
        if 'attachments' in _mailDict[_key]:
            for _filename in _mailDict[_key]['attachments']:
                try:
                    print(_filename, '   attaching...')
                    _file = open(_filename, 'rb')
                    _part= MIMEApplication(_file.read(),Name=os.path.basename(_filename))
                    msg.attach(_part)
                    _file.close()
                except Exception as ex:
                    print (ex)
        print(server.sendmail(_creds['login'], _senders , msg.as_string()))
    server.quit()


if __name__ == '__main__':
    print('works')
    createDir()
    print(getFileName('Vivek', '12345'))
