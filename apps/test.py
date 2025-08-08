from apps.classes import *

app = App("test", priority=999)

@app.handle("*", prerequest=False)
def all(headers:dict, data):
    print(data)

    return data