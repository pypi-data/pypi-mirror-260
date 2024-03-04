import time
import requests
import json
import uuid

#constants
RECONIFY_TRACKER = 'https://track.reconify.com/track'
RECONIFY_UPLOADER = 'https://track.reconify.com/upload'
RECONIFY_MODULE_VERSION = '3.0.0'

#private class
class __CompletionEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

#private variables 
__format = 'universal'
__appKey = None
__apiKey = None
__debug = False
__tracker = RECONIFY_TRACKER
__uploader = RECONIFY_UPLOADER
__user = {}
__session = ''
__sessionTimeout = ''
__trackImages = True

def __convertToJson(str):
    try:
        json.loads(str)
        return json.loads(str)
    except json.JSONDecodeError:
        return str

def __logInteraction(input, output, timestampIn, timestampOut, type):
    if __debug:
        print('Logging interaction')

    #json_output = json.loads(json.dumps(output, cls=__CompletionEncoder))
    json_output = __convertToJson(output)
    payload = {
        "reconify" :{
            "format": __format,
            "appKey": __appKey,
            "apiKey": __apiKey,
            "type": type,
            "version": RECONIFY_MODULE_VERSION,
        },
        "request": input,
        "response": json_output,
        "user": __user,
        "session": __session,
        "sessionTimeout": __sessionTimeout,
        "timestamps": {
            "request": timestampIn,
            "response": timestampOut
        },
    }
    if __debug:
        print('Sending payload: ', payload)
    try:
        requests.post(__tracker, json=payload)
    except requests.exceptions.RequestException as err:
        if __debug:
            print('Send error: ', err)

    return

def config (appKey, apiKey, **options):
    global __appKey
    global __apiKey
    global __debug
    global __tracker
    global __uploader
    global __user
    global __session
    global __sessionTimeout
    global __trackImages

    __appKey = appKey
    __apiKey = apiKey
    if __appKey is None or __apiKey is None:
        raise Exception('An appKey and apiKey are required')
    #optional overides
    if 'debug' in options and options.get('debug') == True:
        __debug = True

    if 'tracker' in options:
        __tracker = options.get('tracker')

    if 'uploader' in options:
        __uploader = options.get('uploader')

    if 'trackImages' in options and options.get('trackImages') == False:
        __trackImages = False

    

def setUser(user):
    global __user
    __user = user

def setSession(session):
    global __session
    __session = session

def setSessionTimeout(sessionTimeout):
    global __sessionTimeout
    __sessionTimeout = sessionTimeout

def getTimestamp():
    return round(time.time()*1000)
    
def logChat(request, response, startTimestamp, endTimeStamp):    
    __logInteraction(request, response, startTimestamp, endTimeStamp, 'chat')
    return