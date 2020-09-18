import logging


class Dijkstra:
    def __init__(self, initial_values, start, goal):
        self.initial_values = initial_values
        self.graph = self.get_graph()
        self.start = start
        self.goal = goal
        self.best_path = self.get_best_path()

    def get_graph(self):
        graph = {}
        for row in self.initial_values:
            origin, destination, cost = row
            if origin not in graph:
                graph[origin] = {}
            if not graph.get(destination):
                graph[destination] = {}
            graph[origin][destination] = cost
        return graph

    def get_best_path(self):
        shortest_distance = {}
        predecessor = {}
        unseen_nodes = self.graph.copy()
        infinity = float("inf")
        path = []
        result = {}
        for node in unseen_nodes:
            shortest_distance[node] = infinity
        shortest_distance[self.start] = 0
        while unseen_nodes:
            min_distance_node = None
            for node in unseen_nodes:
                if min_distance_node is None or shortest_distance[node] < shortest_distance[min_distance_node]:
                    min_distance_node = node
                path_options = self.graph[min_distance_node].items()
                for child_node, cost in path_options:
                    if cost + shortest_distance[min_distance_node] < shortest_distance[child_node]:
                        shortest_distance[child_node] = cost + shortest_distance[min_distance_node]
                        predecessor[child_node] = min_distance_node
            unseen_nodes.pop(min_distance_node)
        current_node = self.goal

        while current_node != self.start:
            try:
                path.insert(0, current_node)
                current_node = predecessor[current_node]
            except KeyError:
                logging.error("Error: Path is not accessible")
                return result

        path.insert(0, self.start)
        total_price = shortest_distance[self.goal]
        if total_price != infinity:
            result = {
                "path": ' > '.join(path),
                "cost": f"R$ {total_price}"
            }
        return result
