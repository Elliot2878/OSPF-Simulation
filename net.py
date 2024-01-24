from ospf_graph import Graph
from router import Router

class Net:
    def __init__(self):
        self.routers = {}
        self.graph = Graph()
        self.edge_list = []  # List to keep track of edges

    def add_router(self, router_id):
        if router_id not in self.routers:
            router = Router(router_id)
            self.routers[router_id] = router
            self.graph.add_vertex(router_id)

    def add_link(self, router1_id, router2_id):
        if router1_id in self.routers and router2_id in self.routers:
            self.routers[router1_id].add_adjacent_router(router2_id)
            self.routers[router2_id].add_adjacent_router(router1_id)
            self.graph.add_edge(router1_id, router2_id)
            self.edge_list.append((router1_id, router2_id))  # Add the edge to the list

    def ping(self, start_id, end_id):
        path = self.graph.find_shortest_path(start_id, end_id)
        return path
