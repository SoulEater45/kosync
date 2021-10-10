import os
import sys
import json
import time
import traceback
import hashlib

from flask import Blueprint, request, jsonify

# Define the blueprint for the flask service
kosync = Blueprint("kosync", __name__, url_prefix="/kosync")

# Database name (for now, only json, later sqlite)
USERSDB = "users.json"

# Should additional output be presented?
DEBUG = True

###########
# Helpers #
###########

def debug_print(msg, debug=False):
    if not debug:
        return
    
    if isinstance(msg, str):
        print(msg, file=sys.stdout)
    elif isinstance(msg, dict):
        if "code" in msg:
            if msg["code"] == 201:
                msg["msg"] = json.dumps(msg["msg"].get_json(), indent=2)
            print(str(msg["code"]) + ": " + msg["msg"], file=sys.stdout)
        else:
            print(json.dumps(msg, indent=2), file=sys.stdout)
    elif hasattr(msg, "is_json") and msg.is_json:
        print(json.dumps(msg.get_json(), indent=2), file=sys.stdout)
    else:
        print("Dunno about the type " + str(type(msg)) + ", lets try it", file=sys.stdout)
        print(msg, file=sys.stdout)


def loadDb():
    if os.path.isfile(USERSDB):
        theFile = open(USERSDB, 'r', encoding='utf-8')
        users = json.load(theFile)
        theFile.close()
    else:
        users = dict()
    return users

def saveDb(users=None):
    theFile = open(USERSDB, 'w+', encoding='utf-8')
    debug_print("Saving database contents: \n" + json.dumps(users, indent=2), DEBUG)
    print(json.dumps(users, indent=2), file=theFile)
    theFile.close()

def getUser(userName, users = None):
    if users == None:
        users = loadDb()
    return users.get(userName)

def addUser(userName, userKey):
    users = loadDb()
    if (getUser(userName, users) != None):
        return False
    users[userName] = dict(username=userName, userkey=userKey)
    saveDb(users)
    return True

def getPosition(username, document):
    user = getUser(username)
    doc = dict()
    documents = user.get('documents')
    if (documents != None):
        doc = documents.get(document)
        if (doc != None):
            doc['document'] = document
    return doc

def updatePosition(username, document, position):
    users = loadDb()
    user = getUser(username, users)
    doc = dict(position)
    timestamp = int(time.time())
    doc['timestamp'] = timestamp
    doc.pop("document", "not_found")
    # doc['percentage'] = position.get('percentage')
    # doc['progress'] = position.get('progress')
    # doc['device'] = position.get('device')
    # doc['device_id'] = position.get('device_id')

    if (user.get('documents') == None):
        user['documents'] = dict()
    user['documents'][document] = doc
    saveDb(users)
    return timestamp

class ServiceError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        super(ServiceError, self).__init__(message)
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        thePayload = self.payload
        if (thePayload):
            # Convert non-iterable payload to an iterable
            try:
                iter(thePayload)
            except:
                thePayload = (thePayload)
        rv = dict(thePayload or ())
        rv['message'] = str(self)
        return rv

def logException(exception):
    kosync.logger.error("".join(traceback.format_exception(type(exception), exception, exception.__traceback__)))

@kosync.errorhandler(ServiceError)
def handle_service_error(error):
    logException(error)
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

def authorizeRequest(request):
    username = request.headers.get("x-auth-user")
    userkey  = request.headers.get("x-auth-key")
    debug_print("Auth request received with:", DEBUG)
    debug_print(dict(un=username, pk=userkey), DEBUG)
    if (username == None or userkey == None):
        raise ServiceError('Unauthorized', status_code=401)

    user = getUser(username)
    if (user == None):
        raise ServiceError('Forbidden', status_code=403)
    if (userkey != user['userkey']):
        raise ServiceError('Unauthorized', status_code=401)
    return user

#######
# API #
#######

@kosync.route("/")
def index():
    return("This is an example")

@kosync.route("/users/create", methods = ["POST"])
def register():
    try:
        if (request.is_json):
            user = request.get_json()
            username = user.get('username')
            userkey = user.get('password')
            msg = jsonify(dict(username=username))
            code = 201
            if (username == None or userkey == None):
                msg = 'Invalid request'
                code = 400
            if (not addUser(username, userkey)):
                msg = 'Username is already registered.'
                code = 409
            debug_print("Registration result: \n", DEBUG)
            debug_print(dict(code=code, msg=msg), DEBUG)
            return msg, code
        else:
            return 'Invalid request', 400
    except Exception as e:
        raise ServiceError('Unknown server error', status_code=500) from e

@kosync.route('/users/auth', methods = ['GET'])
def authorize():
    try:
        authorizeRequest(request)
        return jsonify(dict(authorized='OK')), 200
    except ServiceError as se:
        raise
    except Exception as e:
        raise ServiceError('Unknown server error', status_code=500) from e

@kosync.route('/syncs/progress/<document>', methods = ['GET'])
def getProgress(document):
    try:
        user = authorizeRequest(request)
        position = getPosition(user['username'], document)
        debug_print("GET request made for the current reading state:", DEBUG)
        debug_print(dict(document=document, position=position), DEBUG)
        return jsonify(position), 200
    except ServiceError as se:
        raise
    except Exception as e:
        raise ServiceError('Unknown server error', status_code=500) from e

@kosync.route('/syncs/progress', methods = ['PUT'])
def updateProgress():
    try:
        user = authorizeRequest(request)
        if (request.is_json):
            debug_print("Recieved a current reading position:", DEBUG)
            debug_print(request, DEBUG)
            position = request.get_json()
            document = position.get('document')
            timestamp = updatePosition(user['username'], document, position)
            return jsonify(dict(document = document, timestamp = timestamp)), 200
        else:
            return 'Invalid request', 400
    except ServiceError as se:
        raise
    except Exception as e:
        raise ServiceError('Unknown server error', status_code=500) from e

if __name__ == "__main__":
    print("Running the wrong file, baka...")