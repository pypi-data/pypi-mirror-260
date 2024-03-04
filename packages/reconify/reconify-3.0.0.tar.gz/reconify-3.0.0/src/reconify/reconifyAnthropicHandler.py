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
__format = 'anthropic'
__appKey = None
__apiKey = None
__debug = False
__tracker = RECONIFY_TRACKER
__uploader = RECONIFY_UPLOADER
__user = {}
__session = ''
__sessionTimeout = ''
__trackImages = True

def __logInteraction(input, output, timestampIn, timestampOut, type):
    if __debug:
        print('Logging interaction')

    json_output = json.loads(json.dumps(output, cls=__CompletionEncoder))
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

def config (anthropic, appKey, apiKey, **options):
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


    #override completion create
    anthropic.completions.originalCreate = anthropic.completions.create
    def __reconifyCompletion(*args, **kwargs):
        tsIn = round(time.time()*1000)
        response = anthropic.completions.originalCreate(*args, **kwargs)
        tsOut = round(time.time()*1000)
        __logInteraction(kwargs, response, tsIn, tsOut, 'completion')
        return response 
    anthropic.completions.create = __reconifyCompletion

    #override chat create
    anthropic.messages.originalCreate = anthropic.messages.create
    def __reconifyChat(*args, **kwargs):
        tsIn = round(time.time()*1000)
        response = anthropic.messages.originalCreate(*args, **kwargs)
        tsOut = round(time.time()*1000)
        __logInteraction(kwargs, response, tsIn, tsOut, 'chat')
        return response 
    anthropic.messages.create = __reconifyChat

def setUser(user):
    global __user
    __user = user

def setSession(session):
    global __session
    __session = session

def setSessionTimeout(sessionTimeout):
    global __sessionTimeout
    __sessionTimeout = sessionTimeout