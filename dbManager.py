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

def insertUpdateQuery(_queryString, _values=None):
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
            if _values == None:
                cur.execute(_queryString)
            else:
                cur.execute(_queryString, _values)
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

def registerPatient(_uhid, _patientName, _patientDob, _hospitalName, _patientGender = 'M', _mrd = None, _collectionPoint = None, 
        _collectionDate = None, _labReferenceNumber= None, _departmentName = None, _labName = None, _patientEmail = None, _mobile = None):
    '''
    '''
    _patientId = createPatient(_patientName, _patientDob, _patientGender, _patientEmail, _mobile)
    if _collectionDate:
        if not isinstance(_collectionDate, date):
            raise TypeError('_collectionDate has to be of type date received {0} instead'.type(_collectionDate))
    #CHECK labName
    if _labName:
        _checkQuery = 'SELECT * FROM viewLabs WHERE labName = ?'
        _status = selectQuery(_checkQuery, (_labName,))
        if _status[0]:
            if len(_status[1]) != 1:
                raise Exception('invalid labName: {0}'.format(_labName))
        else:
            if isinstance(_status[1], Exception):
                raise _status[1]
            else: 
                raise Exception(_status[1])
    #CHECK hospitalName
    if _hospitalName:
        _checkQuery = 'SELECT * FROM viewHospitals WHERE hospitalName = ?'
        _status = selectQuery(_checkQuery, (_hospitalName,))
        if _status[0]:
            if len(_status[1]) != 1:
                raise Exception('invalid Hospital Name: {0}'.format(_hospitalName))
        else:
            if isinstance(_status[1], Exception):
                raise _status[1]
            else: 
                raise Exception(_status[1])
    #CHECK departmentName
    if _departmentName:
        _checkQuery = 'SELECT * FROM viewDepartments WHERE departmentName = ?'
        _status = selectQuery(_checkQuery, (_departmentName,))
        if _status[0]:
            if len(_status[1]) != 1:
                raise Exception('invalid Department Name: {0}'.format(department_Name))
        else:
            if isinstance(_status[1], Exception):
                raise _status[1]
            else: 
                raise Exception(_status[1])
 
    _insertQuery = '''INSERT INTO patientRequest (patientId, uhid, mrd, collectionPoint, hospitalName, 
    departmentName, collectionDate, labReferenceNumber, labName) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    _insertTuple = (_patientId, _uhid, _mrd, _collectionPoint, _hospitalName, _departmentName, _collectionDate, _labReferenceNumber, _labName)
    _status = insertUpdateQuery(_insertQuery, _insertTuple)
    if _status[0]:
        return _status[1]
    else:
        if isinstance(_status[1], Exception):
            raise _status[1]
        else: 
            raise Exception(_status[1])

def registerAssays(_requestId, _assayList):
    '''
    '''
    _insertList = [(_requestId, _assayId) for _assayId in _assayList]
    _insertQuery = 'INSERT INTO patientRequestList (requestId, assayId) VALUES (?, ?)'
    _status = insertUpdateMany(_insertQuery, _insertList)
    if _status[0]:
        return True
    else:
        if isinstance(_status[1], Exception):
            raise _status[1]
        else:
            raise Exceptions(_status[1])

def createPatient(_patientName, _patientDob, _patientGender='M', _patientEmail='', _mobile=''):
    '''
    '''
    if _patientGender not in ['M', 'F']:
        raise TypeError('_patientGender has to be either M or F, received {0} instead'.format(_patientGender))
    if not isinstance(_patientDob, date):
        raise TypeError('_dob has to be of type datetime.date, received {0} instead'.format(type(_patientDob)))
    _insertQuery = '''INSERT INTO patientMaster(patientName, patientDob, patientGender, patientEmail, mobile) 
    VALUES (?,?,?,?,?)'''
    _insertTuple = (_patientName, _patientDob, _patientGender, _patientEmail, _mobile)
    _results = insertUpdateQuery(_insertQuery, _insertTuple)
    if _results[0]:
        return _results[1]
    if type(_results[1]) == lite.IntegrityError: #and 'UNIQUE' in _results[1].message:
        raise _results[1]
    else:
        raise Exception(_results[1])

def addHospital(_hospitalName):
    '''
    '''
    _insertQuery = 'INSERT INTO hospitalMaster(hospitalName) VALUES (?)'
    _results = insertUpdateQuery(_insertQuery, (_hospitalName,))
    if _results[0]:
        return True
    if isinstance(_results[1], lite.IntegrityError): #and 'UNIQUE' in _results[1].message:
        _updateQuery = 'UPDATE hospitalMaster SET enabled = 1 WHERE hospitalName = ?'
        _updateResults = insertUpdateQuery(_updateQuery, (_hospitalName,))
        return True
    elif isinstance(_results[1], Exception):
        raise _results[1]
    else:
        raise Exception(_results[1])

def disableHospital(_hospitalName):
    '''
    '''
    _updateQuery = 'UPDATE hospitalMaster SET enabled = 0  WHERE hospitalName = ?'
    _results = insertUpdateQuery(_updateQuery, (_hospitalName,))
    if _results[0]:
        return True
    if  isinstance(_results[1], Exception):
        raise _results[1]
    else:
        raise Exception(_results[1])


def getHospitals():
    '''
    '''
    _results = selectQuery('SELECT * FROM viewHospitals')
    if _results[0]:
        return [e['hospitalName'] for e in _results[1]]
    if isinstance(_results[1], Exception):
        raise _results[1]
    else:
        raise Exception(_result[1])


def addLab(_labName):
    '''
    '''
    _insertQuery = 'INSERT INTO labMaster(labName) VALUES (?)'
    _results = insertUpdateQuery(_insertQuery, (_labName,))
    if _results[0]:
        return True
    if isinstance(_results[1], lite.IntegrityError): #and 'UNIQUE' in _results[1].message:
        _updateQuery = 'UPDATE labMaster SET enabled = 1 WHERE labName = ?'
        _updateResults = insertUpdateQuery(_updateQuery, (_labName,))
        return True
    elif isinstance(_results[1], Exception):
        raise _results[1]
    else:
        raise Exception(_results[1])

def disableLab(_labName):
    '''
    '''
    _updateQuery = 'UPDATE labMaster SET enabled = 0  WHERE labName = ?'
    _results = insertUpdateQuery(_updateQuery, (_labName,))
    if _results[0]:
        return True
    if  isinstance(_results[1], Exception):
        raise _results[1]
    else:
        raise Exception(_results[1])

def getLabs():
    '''
    '''
    _results = selectQuery('SELECT * FROM viewLabs')
    if _results[0]:
        return [e['labName'] for e in _results[1]]
    if isinstance(_results[1], Exception):
        raise _results[1]
    else:
        raise Exception(_result[1])



def addDepartment(_departmentName):
    '''
    '''
    _insertQuery = 'INSERT INTO departmentMaster(departmentName) VALUES (?)'
    _results = insertUpdateQuery(_insertQuery, (_departmentName,))
    if _results[0]:
        return True
    if isinstance(_results[1], lite.IntegrityError): #and 'UNIQUE' in _results[1].message:
        _updateQuery = 'UPDATE departmentMaster SET enabled = 1 WHERE departmentName = ?'
        _updateResults = insertUpdateQuery(_updateQuery, (_departmentName,))
        return True
    elif isinstance(_results[1], Exception):
        raise _results[1]
    else:
        raise Exception(_results[1])


def disableDepartment(_departmentName):
    '''
    '''
    _updateQuery = 'UPDATE departmentMaster SET enabled = 0  WHERE departmentName = ?'
    _results = insertUpdateQuery(_updateQuery, (_departmentName,))
    if _results[0]:
        return True
    if  isinstance(_results[1], Exception):
        raise _results[1]
    else:
        raise Exception(_results[1])


def getDepartments():
    '''
    '''
    _results = selectQuery('SELECT * FROM viewDepartments')
    if _results[0]:
        return [e['departmentName'] for e in _results[1]]
    if isinstance(_results[1], Exception):
        raise _results[1]
    else:
        raise Exception(_result[1])



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
        if isinstance(_results[1], Exception):
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
        if isinstance(_results[1], Exception):
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
    



def getPendingReports(_fromDate = None, _toDate = None):
    '''
    '''
    if _fromDate:
        if isinstance(_fromDate, date):
            if _fromDate > date.today():
                raise ValueError('_fromDate: {0} cannot be greater than current date'.format(_fromDate))
        else:
            raise TypeError('_fromDate should be of type datetime.date, recived {0} instead'.format(type(_fromDate)))
    else:
        _fromDate = date.today().replace(day=1)
    print(_fromDate)
    if _toDate:
        if isinstance(_toDate, date):
            if _toDate < _fromDate:
                raise ValueError('_toDate: {0} cannot be lesser than _fromDate : {1}'.format(_toDate, _fromDate))
            if _toDate < date.today():
                raise ValueError('_toDate: {0} cannot be greater than current date'.format(_toDate))
        else:
            raise TypeError('_fromDate should be of type datetime.date, recived {0} instead'.format(type(_fromDate)))
    else:
        _toDate = date.today()
    print(_fromDate, _toDate)
    _fromDateTime = datetime.combine(_fromDate, datetime.min.time())
    _toDateTime = datetime.combine(_toDate, datetime.max.time())
    _query = 'SELECT * FROM viewPendingPatients WHERE requestTime BETWEEN ? AND ?'
    _selectTuple = (_fromDateTime, _toDateTime)
    _status  = selectQuery(_query, _selectTuple)
    if _status[0]:
        return [{'patientId': _p['patientId'], 'requestId': _p['requestId'], 
            'gender' : _p['patientGender'], 'requestTime' : _p['requestTime']} 
            for _p in _status[1]]
    else:
        if isinstance(_status[1], Exception):
            raise _status[1]
        raise Exception(_status[1])

    


if __name__ == '__main__':
    _a = getPendingReports()
    for e in _a:
        print(e, '\n\n\n')
