import json
from flask import Response

class Error:

    def __new__(cls,message):
        return Response(json.dumps({
            "error":message
        }), status=400,mimetype='application/json')

    def __init__(self,message):
        pass