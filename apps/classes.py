class App:
    def __init__(self, name:str, priority:int=5):
        self.name = name
        self.priority = priority
        self.pre_routes = {}
        self.post_routes = {}

    def handle(self, route, prerequest:bool=True):
        def decorator(func):
            if prerequest:
                self.pre_routes[route] = func
            else:
                self.post_routes[route] = func

            return func
        return decorator

    def _predispatch(self, route, data=None, headers={}):
        if "*" in self.pre_routes:
            handler = self.pre_routes["*"]
        elif route in self.pre_routes:
            handler = self.pre_routes[route]
        else:
            return data

        heartbeat = handler(
            headers=headers,
            data=data
        )

        return heartbeat
    
    def _postdispatch(self, route, data=None, headers={}):
        if "*" in self.post_routes:
            handler = self.post_routes["*"]
        elif route in self.post_routes:
            handler = self.post_routes[route]
        else:
            return data

        heartbeat = handler(
            headers=headers,
            data=data
        )

        return heartbeat