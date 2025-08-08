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
        if "*" in list(self.routes.keys()):
            handler = self.routes["*"]
        else:
            handler = self.routes[route]

        heartbeat = handler(
            headers=headers,
            data=data
        )

        return heartbeat