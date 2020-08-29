#!env/bin/python
import sqlite3 as lite
from datetime import datetime
import os



def getCursor(_path=''):
    con = None
    cur = None
    try:
        con = lite.connect(os.path.join(_path,'nimhans.db'), detect_types=lite.PARSE_DECLTYPES)#MODIFY LATER IF REQUIRED BASED ON INSANCE
        con.isolation_level = None #want autocommit only when BEGIN STATEMENT IS MISSING - CONFUSING DOCUMENTATION
        con.row_factory = lite.Row
        cur = con.cursor()
        cur.execute('PRAGMA foreign_keys = ON;')
    except Exception as err:
        print('Error: ', err)
    return con, cur

def selectQuery(_queryString, _values=None):
    con, cur = getCursor()
    _rows = []
    if cur!= None and con != None:
        try:
            if _values == None:
                cur.execute(_queryString)
            else:
                cur.execute(_queryString, _values)
                print((_queryString, _values))
            _rows = cur.fetchall()
            return [True, _rows]
        except Exception as ex:
            print ('Error exeuting \n{0},{1} \n {2}'.format(_queryString, _values, ex))
            return [False, ex]
        finally:
            cur.close()
            con.close()

def getAssayList():
    _rows = selectQuery('SELECT * FROM assayMaster WHERE enabled = 1 ORDER BY assayName')
    if(_rows[0]):
        return [{e['assayId'] : {'Name': e['assayName'], 'Description': e['assayDescription']}} for e in _rows[1]]
    return []


def disableAssay(_assayId):
    '''
    _assayId is integer
    if any other type is sent we will throw expception

    '''
    if _assayId:
        return False
    return True


def addAssay(_name, _description=''):
    '''
    '''
    if _name:
        return False
    return True

def getAntibodies(_assayId=None):
    '''
    '''
    if _assayId:
        return {antibodyId: { 'Name' : antibodyName, 'Options': {optionId : optionName }}}
    return {assayId:{antibodyId: { 'Name' : antibodyName, 'Options': {optionId : optionName }}}}
    

if __name__ == '__main__':
    print('works')
    _assays = getAssayList()
    for _assay in _assays:
        _id, _details = next(iter(_assay.items()))

