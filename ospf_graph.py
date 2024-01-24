import heapq

class Graph:
    def __init__(self):
        self.lsdb = {}  # Link-State Database

    def add_vertex(self, vertex_id):
        if vertex_id not in self.lsdb:
            self.lsdb[vertex_id] = {}
            print(f"LSA: Initialized LSDB for router {vertex_id}.")

    def add_edge(self, node1_id, node2_id, cost=1):
        if node1_id not in self.lsdb or node2_id not in self.lsdb:
            raise Exception("Both nodes must be in the LSDB before adding an edge.")
        
        self.lsdb[node1_id][node2_id] = cost
        self.lsdb[node2_id][node1_id] = cost
        print(f"LSA: Link state updated for routers {node1_id} and {node2_id} with cost {cost}.")
        self.flood_lsa(node1_id, node2_id, cost)


    def flood_lsa(self, source_id, neighbor_id, cost, visited=None):
        if visited is None:
            visited = set()

        visited.add(source_id)

        # Flood LSA to direct neighbors of the source
        for node in self.lsdb:
            if node != source_id and neighbor_id in self.lsdb[node] and node not in visited:
                # Update the LSDB for the neighbor
                self.lsdb[node][source_id] = cost
                self.lsdb[node][neighbor_id] = cost
                print(f"LSA: Router {node} updated its LSDB with link {source_id}-{neighbor_id}.")
                # Further propagate the LSA
                self.flood_lsa(node, source_id, cost, visited)


    def find_shortest_path(self, start_id, end_id):
        if start_id not in self.lsdb or end_id not in self.lsdb:
            return []
        
        distances = {vertex: float('infinity') for vertex in self.lsdb}
        previous_nodes = {vertex: None for vertex in self.lsdb}
        distances[start_id] = 0
        pq = [(0, start_id)]

        while pq:
            current_distance, current_vertex = heapq.heappop(pq)

            for neighbor, weight in self.lsdb[current_vertex].items():
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_vertex
                    heapq.heappush(pq, (distance, neighbor))

        path = []
        current_vertex = end_id
        while current_vertex != start_id and current_vertex is not None:
            path.insert(0, current_vertex)
            current_vertex = previous_nodes[current_vertex]

        if path:
            path.insert(0, start_id)
        return path