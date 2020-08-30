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



def insertUpdateMany(_queryString, _values):
    """[summary]

    Arguments:
        _queryString {[type]} -- [description]
        _values {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    con, cur = getCursor()
    print("Yep")
    print (_queryString, _values)
    if cur!= None and con != None:
        try:
            cur.execute('BEGIN')
            cur.executemany(_queryString, _values)
            cur.execute ('COMMIT')
            return [True,'']
        except Exception as ex:
            cur.execute('ROLLBACK')
            print ('Error exeuting \n{0},{1} \n {2}'.format( _queryString, _values, ex))
            return [False, ex]
        finally:
            cur.close()
            con.close()

def insertUpdateQuery(_queryString, _values):
    """[summary]

    Arguments:
        _queryString {[type]} -- [description]
        _values {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    con, cur = getCursor()
    print("Yep")
    print (_queryString, _values)
    if cur!= None and con != None:
        try:
            cur.execute('BEGIN')
            cur.execute (_queryString, _values)
            lastrowid = cur.lastrowid
            cur.execute ('COMMIT')
            return [True,lastrowid]
        except Exception as ex:
            cur.execute('ROLLBACK')
            print ('Error exeuting \n{0},{1} \n {2}'.format( _queryString, _values, ex))
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
    if type(_assayId) == int:
        _results = selectQuery('SELECT * FROM assayMaster WHERE assayId = ?', (_assayId,))
        if _results[0]:
            if len(_results[1]) == 0:
                raise ValueError('assayId {0} invalid'.format(_assayId))
        _query = 'UPDATE assayMaster SET enabled = 0 WHERE assayId = ?'
        _status = insertUpdateQuery(_query, (_assayId,))
        if _status[0]:
            return True
        else:
            return False
    else:
        raise TypeError('assayId needs to be integer got {0}, {1}'.format(type(_assayId), _assayId))


def addAssay(_assayName, _assayDescription=''):
    '''
    '''
    if(type(_assayName) != str):
        raise TypeError('assayName needs to be string got {0}, {1}'.format(type(_assayName), _assayName))
    _query = 'INSERT INTO assayMaster (assayName) VALUES (?)'
    _insertTuple = (_assayName,)
    if _assayDescription:
        if(type(_assayDescription) != str):
            raise TypeError('description needs to be string got {0}, {1}'.format(type(_assayDescription), _assayDescription))
        _query = 'INSERT INTO assayMaster (assayName, assayDescription) VALUES (?,?)'
        _insertTuple = (_assayName, _assayDescription)
    T_results = insertUpdateQuery(_query, _insertTuple)
    if _results[0]:
        return _results[1]
    return -1

 


def getAntiBodies(_assayId=None):
    '''
    '''
    if _assayId:
        if type(_assayId) != int:
            raise TypeError('assayId needs to be integer got {0}, {1}'.format(type(_assayId), _assayId))
        _query = 'SELECT * FROM viewAntiBodyOptions WHERE assayId = ?'
        _results = selectQuery(_query, (_assayId,))
        if _results[0]:
            _ret = {}
            for _row in _results[1]:
                _antiBodyId = _row['antiBodyId']
                _antiBodyName  = _row['antiBody']
                _optionId = _row['optionId']
                _option = _row['optionText']
                if _antiBodyId in _ret:
                    _ret[_antiBodyId]['Options'][_optionId] = _option
                else:
                    _ret[_antiBodyId] = {'Name': _antiBodyName, 'Options': {_optionId : _option}}
            return _ret
        else:
            raise Exception(_results[1])
    else:
        _query = 'SELECT * FROM viewAntiBodyOptions'
        _results = selectQuery(_query,(_assayId))
        if _results[0]:
            _ret = {}
            for _row in _results[1]:
                _assayId = _row['assayId']
                _antiBodyId = _row['antiBodyId']
                _antiBodyName  = _row['antiBody']
                _optionId = _row['optionId']
                _option = _row['optionText']
                if _assayId in _ret:
                    if _antiBodyId in _ret[_assayId]:
                        _ret[_assayId][_antiBodyId]['Options'][_optionId] = _option
                    else:
                        _ret[_assayId][_antiBodyId] = {'Name': _antiBodyName, 'Options': {_optionId : _option}}
                else:
                    _ret[_assayId] = {_antiBodyId : { 'Name' : _antiBodyName, 'Options': {_optionId : _option}}}
            return _ret
    

if __name__ == '__main__':
    print('works')
    _assays = getAssayList()
    for _assay in _assays:
        _id, _details = next(iter(_assay.items()))
        print('assayId:{0}\nassayName:{1}\nassayDescription{2}\n\n'.format(_id, _details['Name'], _details['Description']))
    try:
        disableAssay('vivek')
    except Exception as ex:
        print(ex)
    try:
        disableAssay(45)
    except Exception as ex:
        print(ex)
    _assays = getAssayList()
    try:
        disableAssay(1)
    except Exception as ex:
        print(ex)
    _assays = getAssayList()
    for _assay in _assays:
        _id, _details = next(iter(_assay.items()))
        print('assayId:{0}\nassayName:{1}\nassayDescription{2}\n\n'.format(_id, _details['Name'], _details['Description']))
    try:
        _assayId = addAssay('Vivek1')
        print('Vivek1:', _assayId)
    except Exception as ex:
        print(ex)
    try:
        _assayId = addAssay('Vivek1', 'whattay vivek')
        print('Vivek1:', _assayId)
    except Exception as ex:
        print(ex)
    _assays = getAssayList()
    for _assay in _assays:
        _id, _details = next(iter(_assay.items()))
        print('assayId:{0}\nassayName:{1}\nassayDescription{2}\n\n'.format(_id, _details['Name'], _details['Description']))
    _results = getAntiBodies()
    for e in _results:
        print(e,'\n', _results[e], '\n\n')

