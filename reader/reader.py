import json

def __unicodeToStr(data):
    #convert dict
    if isinstance(data, dict):
        return { __unicodeToStr(key): __unicodeToStr(value) for key, value in data.iteritems() }
    #convert list
    if isinstance(data, list):
        print data
        return [ __unicodeToStr(val) for val in data ]
    #convert unicode to str
    if isinstance(data, unicode):
        return data.encode('utf-8')

    return data

def read_file(jsonParams):
    jsonFile = open(jsonParams, 'r').read()
    parsedJSON = json.loads(jsonFile)
    return parsedJSON
