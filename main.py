from flask import Flask, request, Response, redirect
import concurrent.futures
from os import environ
import pytoml as toml
import apps
import requests

app = Flask(__name__)

with open("config.toml", "r", encoding="utf-8") as f:
    raw_config = f.read()
    config = toml.loads(raw_config)

environ["WAKAMITM_CONFIG"] = raw_config

enabled_apps = [app for app in apps.apps if config.get("apps",{}).get(app.name,{}).get("enabled", False)]

@app.route('/', defaults={'path': ''}, methods=["GET", "DELETE", "POST"])
@app.route('/<path:path>', methods=["GET", "DELETE", "POST"])
def catch_all(path):
    method = request.method

    if path == "" and method == "GET":
        return redirect("https://github.com/MathiasDPX/wakatime_mitm")

    if path == "healthcheck" and method == "GET":
        return {"status": "OK"}

    args = request.args
    cookies = request.cookies
    headers = {key: value for key, value in request.headers if key.lower() != 'host'}
    headers["X-Middleware-Apps"] = ",".join([app.name for app in enabled_apps])

    if method == "POST":
        data = request.get_json()
    else:
        data = request.get_data()

    # Preprocess heartbeats
    for app in enabled_apps:
        data = app._predispatch(path, data, headers)

    # Send heartbeats in concurrence for faster response
    def send_heartbeat(backend):
        newheaders = headers.copy() # uuhh if it's not a copy it's not work 
        newheaders["Authorization"] = backend[1]

        resp = requests.request(
            method=method,
            url=backend[0]+path,
            headers=newheaders,
            params=args,
            json=data if method == "POST" and data else None,
            data=data if method != "POST" else None,
            cookies=cookies,
            allow_redirects=False,
            stream=True
        )

        return resp
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(send_heartbeat, config.get("redirector", {}).get("backends", [])))

    response = results[0]
    resp_data = response.content

    # Postprocess response
    for app in enabled_apps:
        resp_data = app._postdispatch(path, resp_data, response.headers)

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    response_headers = [(k, v) for k, v in response.raw.headers.items() if k.lower() not in excluded_headers]

    return Response(resp_data, status=response.status_code, headers=response_headers)

if __name__ == "__main__":
    app.run(host="0.0.0.0")