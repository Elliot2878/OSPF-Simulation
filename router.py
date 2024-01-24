class Router:
    def __init__(self, router_id):
        self.router_id = router_id
        self.adjacent_routers = []

    def add_adjacent_router(self, router_id):
        if router_id not in self.adjacent_routers:
            self.adjacent_routers.append(router_id)
