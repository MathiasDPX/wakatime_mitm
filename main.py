from flask import Flask, request, Response
from os import environ
import pytoml as toml
import apps
import requests

app = Flask(__name__)

with open("config.toml", "r", encoding="utf-8") as f:
    raw_config = f.read()
    config = toml.loads(raw_config)

environ["WAKAMITM_CONFIG"] = raw_config

@app.route('/', defaults={'path': ''}, methods=["GET", "DELETE", "POST"])
@app.route('/<path:path>', methods=["GET", "DELETE", "POST"])
def catch_all(path):
    method = request.method
    url = f"{config.get('redirect-url', '')}{path}"
    headers ={key: value for key, value in request.headers if key.lower() != 'host'}

    if method == "POST":
        data = request.get_json()
    else:
        data = request.get_data()

    for app in apps.apps:
        if config.get("apps",{}).get(app.name,{}).get("enabled", False):
            data = app._predispatch(path, data, headers)

    resp = requests.request(
        method=method,
        url=url,
        headers=headers,
        params=request.args,
        json=data if method == "POST" and data else None,
        data=data if method != "POST" else None,
        cookies=request.cookies,
        allow_redirects=False,
        stream=True
    )

    resp_data = resp.content

    for app in apps.apps:
        if config.get("apps",{}).get(app.name,{}).get("enabled", False):
            resp_data = app._postdispatch(path, resp_data, resp.headers)

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    response_headers = [(k, v) for k, v in resp.raw.headers.items() if k.lower() not in excluded_headers]

    return Response(resp_data, status=resp.status_code, headers=response_headers)

if __name__ == "__main__":
    app.run(host="0.0.0.0")