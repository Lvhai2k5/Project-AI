import heapq

class UniformCostSearch:
    def __init__(self, graph):
        self.graph = graph

    def find_path(self, start, end):
        # Khởi tạo khoảng cách và danh sách ưu tiên
        distances = {node: float('infinity') for node in self.graph}
        distances[start] = 0
        previous = {node: None for node in self.graph}
        pq = [(0, start)]  # (chi phí, nút)

        while pq:
            current_cost, current_node = heapq.heappop(pq)

            if current_node == end:
                break

            if current_cost > distances[current_node]:
                continue

            for neighbor, weight in self.graph[current_node].items():
                new_cost = current_cost + weight

                if new_cost < distances[neighbor]:
                    distances[neighbor] = new_cost
                    previous[neighbor] = current_node
                    heapq.heappush(pq, (new_cost, neighbor))

        # Xây dựng đường đi
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()

        return path, distances[end]