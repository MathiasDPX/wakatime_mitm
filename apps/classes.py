class App:
    def __init__(self, name:str, priority:int=5):
        self.name = name
        self.priority = priority
        self.routes = {}

    def handle(self, route):
        def decorator(func):
            self.routes[route] = func
            return func
        return decorator

    def _dispatch(self, route, data=None, headers={}):
        if "*" in self.routes:
            handler = self.routes["*"]
        elif route in self.routes:
            handler = self.routes[route]
        else:
            return data

        heartbeat = handler(
            headers=headers,
            data=data
        )

        return heartbeat