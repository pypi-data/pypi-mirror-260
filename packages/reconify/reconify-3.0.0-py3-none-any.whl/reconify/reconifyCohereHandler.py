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
__format = 'cohere'
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

    #json_output = json.loads(json.dumps(output, cls=__CompletionEncoder))
    json_output = None 
    if type == 'completion':
        json_output = {'generations': list(map(lambda x: dict(vars(x)), output))}
    else:
        json_output = dict(vars(output))
        if 'client' in json_output:
            del json_output['client']

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

def config (cohere, appKey, apiKey, **options):
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

    #override chat create
    cohere.originalChat = cohere.chat
    def __reconifyChat(*args, **kwargs):
        tsIn = round(time.time()*1000)
        response = cohere.originalChat(*args, **kwargs)
        tsOut = round(time.time()*1000)
        __logInteraction(kwargs, response, tsIn, tsOut, 'chat')
        return response 
    cohere.chat = __reconifyChat 

    #override completion create
    cohere.originalGenerate = cohere.generate
    def __reconifyGenerate(*args, **kwargs):
        tsIn = round(time.time()*1000)
        response = cohere.originalGenerate(*args, **kwargs)
        tsOut = round(time.time()*1000)
        __logInteraction(kwargs, response, tsIn, tsOut, 'completion')
        return response 
    cohere.generate = __reconifyGenerate

def setUser(user):
    global __user
    __user = user

def setSession(session):
    global __session
    __session = session

def setSessionTimeout(sessionTimeout):
    global __sessionTimeout
    __sessionTimeout = sessionTimeout