from apps.classes import *
from flask import abort
import pytoml as toml
import base64
import os

app = App("auth", priority=0)

def readToken(rawtoken:str) -> str:
    if rawtoken.startswith("Basic "):
        b64_token = rawtoken.replace("Basic ", "", 1)
        token = base64.b64decode(b64_token)
        return token.decode()

    elif rawtoken.startswith("Bearer "):
        token = rawtoken.replace("Bearer ", "")
        return token

    return rawtoken

@app.handle("*")
def verify_token(headers:dict, data:dict):
    config = toml.loads(os.environ.get("WAKAMITM_CONFIG", ""))
    tokens = config.get("apps", {}).get("auth", {}).get("tokens", [])

    auth_header = headers.get("Authorization", "none")
    token = readToken(auth_header)

    if token not in tokens:
        abort(403)
        return {}

    return data