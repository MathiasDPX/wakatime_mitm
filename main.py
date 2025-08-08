from flask import Flask, request, Response
import requests
import re

app = Flask(__name__)

class App:
    def __init__(self, name):
        self.name = name
        self.routes = {}

    def handle(self, route):
        def decorator(func):
            self.routes[route] = func
            return func
        return decorator

    def dispatch(self, route, data=None):
        handler = self.routes[route]
        heartbeat = handler(data)
        print(heartbeat)

        return heartbeat
    
leetcode = App("LeetCode.nvim")

@leetcode.handle("users/current/heartbeats.bulk")
@leetcode.handle("users/current/heartbeats")
def leetcode_change_proj_name(data:dict):
    for entry in data:
        match = re.match(r'\/.+\/\.local\/share\/nvim\/leetcode\/(\d+)\.', entry.get("entity", ""))

        if match:
            id = match.group(1)
            entry["project"] = f"LeetCode {id}"
            print(entry["project"])

    return data

apps = [leetcode]

@app.route('/', defaults={'path': ''}, methods=["GET", "DELETE", "POST"])
@app.route('/<path:path>', methods=["GET", "DELETE", "POST"])
def catch_all(path):
    method = request.method
    url = f"https://hackatime.hackclub.com/api/hackatime/v1/{path}"
    headers = {key: value for key, value in request.headers if key.lower() != 'host'}
    data = request.get_json()


    if method == "POST":
        for app in apps:
            data = app.dispatch(path, data)
            
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

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    response_headers = [(k, v) for k, v in resp.raw.headers.items() if k.lower() not in excluded_headers]

    return Response(resp.content, status=resp.status_code, headers=response_headers)

app.run(host="0.0.0.0")