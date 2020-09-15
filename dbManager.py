#!env/bin/python
import sqlite3 as lite
from datetime import datetime
from datetime import date
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
    _results = insertUpdateQuery(_query, _insertTuple)
    if _results[0]:
        return _results[1]
    else:
        if type(_results[1]) == lite.IntegrityError: #and 'UNIQUE' in _results[1].message:
            _query = 'UPDATE assayMaster SET enabled = 1, assayDescription = ? WHERE assayName = ?'
            _updateResults = insertUpdateQuery(_query, (_assayDescription, _assayName))
            if _updateResults[0]:
                #we need to get assayId
                _query = 'SELECT assayId from assayMaster where assayName = ?'
                _assayIdResults = selectQuery(_query, (_assayName,))
                if _assayIdResults[0]:
                    return _assayIdResults[1][0]['assayId']
        return -1

def disableAntiBody(_assayId, _antiBodyId):
    '''
    '''
    if type(_assayId) != int:
        raise TypeError('assayId needs to be integer got {0}, {1}'.format(type(_assayId), _assayId))
    if(type(_antiBodyId) != int):
        raise TypeError('assayName needs to be integer got {0}, {1}'.format(type(_assayName), _assayName))
    _results = selectQuery('SELECT * FROM antiBodies WHERE assayId = ? AND antiBodyId = ?', (_assayId, _antiBodyId))
    if _results[0]:
        if len(_results[1]) == 0:
            raise ValueError('assayId {0} invalid'.format(_assayId))
    _query = 'UPDATE antiBodies SET enabled = 0 WHERE assayId = ? AND antiBodyId = ?'
    _status = insertUpdateQuery(_query, (_assayId, _antiBodyId))
    if _status[0]:
        return True
    else:
        return False
  
def addAntiBody(_assayId, _antiBody):
    '''
    '''
    if type(_assayId) != int:
        raise TypeError('assayId needs to be integer got {0}, {1}'.format(type(_assayId), _assayId))
    if(type(_antiBody) != str):
        raise TypeError('assayName needs to be string got {0}, {1}'.format(type(_assayName), _assayName))
    _query = 'INSERT INTO antiBodies (assayId, antiBody) VALUES (?,?)'
    _status = insertUpdateQuery(_query, (_assayId, _antiBody))
    if _status[0]:
        return _status[1] #antiBodyId
    else:
        if type(_status[1]) == lite.IntegrityError: #and 'UNIQUE' in _results[1].message:
            if 'UNIQUE' in str(_status[1]):
                _query = 'UPDATE antiBodies SET enabled = 1 WHERE assayId = ? AND antiBody = ?'
                _updateStatus = insertUpdateQuery(_query, (_assayId, _antiBody))
                if _updateStatus[0]:
                    #we need to get assayId
                    _query = 'SELECT antiBodyId FROM antiBodies WHERE assayId= ? AND antiBody = ?'
                    _antiBodyIdResults = selectQuery(_query, (_assayId, _antiBody))
                    if _antiBodyIdResults[0]:
                        return _antiBodyIdResults[1][0]['antiBodyId']
    return -1

def disableOption(_assayId, _antiBodyId, _optionId):
    '''
    '''
    _checkQuery = 'SELECT * FROM antiBodyOptions WHERE assayID = ? AND antiBodyId = ? AND optionId = ?'
    _results = selectQuery(_checkQuery, (_assayId, _antiBodyId, _optionId))
    if _results[0]:
        if len(_results[1]) != 1:
            raise Exception ('No such combination of assayId:{0}, antiBodyId:{1} and optionId:{2}'.format(_assayId, _antiBodyId, _optionId))
        if _results[1][0]['enabled']:
            _query = 'UPDATE antiBodyOptions SET enabled = 0 WHERE optionId = ?'#WE DONT NEED THE OTHER TWO
            _status = insertUpdateQuery(_query, (_optionId,))
            if _status[0]:
                return _status[1]
            else:
                return -1
    else:
        if isInstance(_results[1], Exception):
            raise _results[1]
        raise Exception(_results[1])




def addOption(_assayId, _antiBodyId, _option):
    '''
    check if _assayId and _antiBodyId are enabled
    check if _option already exists
    insert into antiBodyOptions
    or update antiBodyOption
    '''
    _checkQuery = 'SELECT * FROM antiBodies WHERE assayId = ? AND antiBodyId = ?'
    _results = selectQuery(_checkQuery, (_assayId, _antiBodyId))
    if _results[0]:
        if len(_results[1]) ==  1:
            if _results[1][0]['enabled'] == 0:
                raise Exception('No such enabled combination of assayId:{0} and antiBodyId{0}'.format(_assayId, _antiBodyId))
            _insertQuery = 'INSERT INTO antiBodyOptions (assayId, antiBodyId, optionText) VALUES (?,?,?)'
            print('inserting ' , _insertQuery)
            _status = insertUpdateQuery(_insertQuery, (_assayId, _antiBodyId, _option))
            print(_status)
            if _status[0]:
                return _status[1]
            else:
                if type(_status[1]) == lite.IntegrityError: #and 'UNIQUE' in _results[1].message:
                    if 'UNIQUE' in str(_status[1]):
                        _query = 'UPDATE antiBodyOptions SET enabled = 1 WHERE assayId = ? AND antiBodyId = ? AND optionText = ?'
                        _updateStatus = insertUpdateQuery(_query, (_assayId, _antiBodyId, _option))
                        if _updateStatus[0]:
                            #we need to get assayId
                            _query = 'SELECT optionId FROM antiBodyOptions WHERE assayId= ? AND antiBodyId = ? AND optionText = ?'
                            _optionIdResults = selectQuery(_query, (_assayId, _antiBodyId, _option))
                            print('option?1')
                            if _optionIdResults[0]:
                                print('option?2')
                                return _optionIdResults[1][0]['optionId']
        else:
            raise Exception('No such combination of assayId:{0} and antiBodyId:{1}'.format(_assayId, _antiBodyId))
    else:
        if isInstance(_results[1], Exception):
            raise _results[1]
        raise Exception(_results[1])


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
    addAntiBody(1, 'buffalo')
    disableAntiBody(1,11)
    addAntiBody(1, 'buffalo')
    print('dont with this.')
    _id = 0
    try:
        _id =addOption(1,11,'option#1')
        print(_id)
    except Exception as ex:
        print(ex)
    try:
        disableOption(1,10,_id)
    except Exception as ex:
        print(ex)
    try:
        disableOption(1,11,_id)
        _id =addOption(1,11,'option#1')
        print(_id)
    except Exception as ex:
        print(ex)
