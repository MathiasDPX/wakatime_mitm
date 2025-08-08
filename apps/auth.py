from apps.classes import *
from flask import abort
import pytoml as toml
import os

app = App("auth", priority=0)

@app.handle("*")
def verify_token(headers:dict, data:dict):
    config = toml.loads(os.environ.get("WAKAMITM_CONFIG", ""))
    tokens = config.get("apps", {}).get("auth", {}).get("tokens", [])

    auth_header = headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    token = auth_header.strip()

    if auth_header not in tokens:
        abort(403)
        return {}

    return data