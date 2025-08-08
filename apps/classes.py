class App:
    def __init__(self, name):
        self.name = name
        self.routes = {}

    def handle(self, route):
        def decorator(func):
            self.routes[route] = func
            return func
        return decorator

    def _dispatch(self, route, data=None):
        handler = self.routes[route]
        heartbeat = handler(data)
        print(heartbeat)

        return heartbeat