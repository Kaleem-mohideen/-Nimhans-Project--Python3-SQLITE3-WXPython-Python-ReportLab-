#!env/bin/python
import sys
import os

from dbManager import selectQuery
from dbManager import insertUpdateQuery

if __name__ == '__main__':
    _list = os.listdir(sys.argv[1])
    _xmlFiles = [e for e in _list if e.endswith('.xml') and os.path.isfile(os.path.join(sys.argv[1],e))]
    print(_xmlFiles)
    _antiBodies = selectQuery('SELECT * FROM viewAntiBodyOptions GROUP BY antiBodyId')
    if _antiBodies[0]:
        pass
    else:
        if isinstance(_antiBodies[1], Exception):
            raise _antiBodies[1]
        raise Exception(_antiBodies[1])
    _assayDict = {}
    for e in _antiBodies[1]:
        _assayId = e['assayId']
        _assayName = e['assayName']
        _antiBodyId = e['antiBodyId']
        _antiBodyName = e['antiBody']
        if _assayId in _assayDict:
            _assayDict[_assayId]['antiBodies'][_antiBodyId] = _antiBodyName
        else:
            _assayDict[_assayId] = {'assayName': _assayName, 'antiBodies' : {_antiBodyId : _antiBodyName}}
    
    _assayString = '\n'.join([str(e[0] + 1) + '. '+ str(_assayDict[e[1]]['assayName']) for e in enumerate(sorted(_assayDict.keys()))])
    _assayIds = { e[0]+1 : e[1] for e in enumerate(sorted(_assayDict.keys()))}
    for e in _xmlFiles:
        _path =os.path.join(sys.argv[1],e) 
        _xml = open(_path, 'rb').read().decode('utf-8')
        _flag = True
        while _flag:
            print(_path, '\n\n')
            print(_xml, '\n\n')
            print (_assayString)
            print('please choose appropriate assay\n or i to ignore')
            _assayInput = input('\n')
            if _assayInput.strip() == 'i':
                _flag = False
                continue
            print(_assayInput)
            if _assayInput.isdigit() and int(_assayInput) in _assayIds:
                _assayId = _assayIds[int(_assayInput)]
                print('\n\n')
                print('chosen {0}'.format(_assayDict[_assayId]['assayName']))
                _antiBodyIds = { e[0] +1 : e[1] for e in enumerate( sorted(_assayDict[_assayId]['antiBodies'].keys()))}
                _antiBodyString = '\n'.join([ str(e[0] +1) +'. ' +  _assayDict[_assayId]['antiBodies'][e[1]] 
                                        for e in enumerate( sorted(_assayDict[_assayId]['antiBodies'].keys()))])
                print(_antiBodyString)
                print('Please choose the appropriate antibody\n or i to ignore')
                _antiBodyInput = input('\n')
                if _antiBodyInput.strip() == 'i':
                    _flag = False
                    continue
                if _antiBodyInput.isdigit() and int(_antiBodyInput) in _antiBodyIds:
                    _antiBodyId = _antiBodyIds[int(_antiBodyInput)]
                    _updateQuery = 'UPDATE antiBodies SET comments = ? WHERE antiBodyId = ?'
                    _status = insertUpdateQuery(_updateQuery, (_xml, _antiBodyId))
                    input('huh???\n\n\n')
                    _flag = False
                else:
                    print('Only numbers between 1 and {0} allowed\n\n\n'.format(len(_antiBodyIds)))
            else:
                print('Only numbers between 1 and {0} allowed\n\n\n'.format(len(_assayIds)))

