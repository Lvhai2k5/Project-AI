from collections import deque
import time
from ReadFile import read_distance_file_blind, read_route_file, read_abbreviation_file
import math
from heapq import heappush, heappop
import random
import numpy as np
from ucs import UniformCostSearch

# Đường dẫn đến các file dữ liệu
distance_file_path = 'distance.txt'
route_file_path = 'route.txt'
abbreviation_file_path = 'abbreviation.txt'

# Tải dữ liệu từ các file
distance_graph = read_distance_file_blind(distance_file_path)
route_graph = read_route_file(route_file_path)
abbreviations = read_abbreviation_file(abbreviation_file_path)
print("Đồ thị khoảng cách:", distance_graph)
print("Đồ thị tuyến đường:", route_graph)
print("Danh sách viết tắt:", abbreviations)

# Kiểm tra dữ liệu
if not distance_graph or not route_graph:
    print("Lỗi: Không có dữ liệu trong distance.txt hoặc route.txt")
    exit(1)

# Xây dựng đồ thị
graph = {}
for edge in distance_graph:
    if len(edge) < 3:
        print(f"Cảnh báo: Dữ liệu cạnh không hợp lệ: {edge}")
        continue
    src, dest, distance = edge
    try:
        distance = float(distance)
    except ValueError:
        print(f"Cảnh báo: Khoảng cách không hợp lệ: {distance} trong {src} -> {dest}")
        continue
    # Tìm mã đường từ route.txt
    road_code = None
    for r_edge in route_graph:
        if len(r_edge) != 3:
            print(f"Cảnh báo: Dữ liệu tuyến đường không hợp lệ: {r_edge}")
            continue
        if (r_edge[0] == src and r_edge[1] == dest) or (r_edge[0] == dest and r_edge[1] == src):
            road_code = r_edge[2]
            break
    if not road_code:
        print(f"Cảnh báo: Không tìm thấy mã đường cho cạnh {src} -> {dest} trong route.txt")
        continue
    road = abbreviations.get(road_code, road_code)  # Ánh xạ sang tên đầy đủ
    if road == road_code:
        print(f"Cảnh báo: Không tìm thấy tên đường cho mã {road_code} trong abbreviation.txt")
    if src not in graph:
        graph[src] = {}
    if dest not in graph:
        graph[dest] = {}
    graph[src][dest] = {'road': road, 'distance': distance}
    graph[dest][src] = {'road': road, 'distance': distance}
print("Đồ thị:", graph)

# Kiểm tra đồ thị
if not graph:
    print("Lỗi: Đồ thị rỗng. Vui lòng kiểm tra dữ liệu trong distance.txt và route.txt")
    exit(1)

# Hàm gộp đường đi
def simplify_path(path, graph):
    """Gộp các đoạn đường liên tiếp có cùng tên đường thành một đoạn."""
    if not path or len(path) < 2:
        return []
    simplified = []
    i = 0
    while i < len(path) - 1:
        start = path[i]
        next_node = path[i + 1]
        road = graph[start].get(next_node, {}).get('road', '')
        current_road = road
        end_node = next_node
        j = i + 1
        while j < len(path) - 1:
            curr_node = path[j]
            next_node = path[j + 1]
            next_road = graph[curr_node].get(next_node, {}).get('road', '')
            if next_road != current_road or not next_road:
                break
            end_node = next_node
            j += 1
        simplified.append((start, end_node, current_road))
        i = j
    return simplified

# Hàm tính tổng khoảng cách
def calculate_distance(path, graph):
    """Tính tổng khoảng cách của một đường đi."""
    total_dist = 0
    for i in range(len(path) - 1):
        src, dest = path[i], path[i + 1]
        edge_info = graph.get(src, {}).get(dest)
        if edge_info and 'distance' in edge_info:
            total_dist += edge_info['distance']
    return total_dist

# Thuật toán BFS
def bfs(graph, start, goal):
    """Tìm đường đi ngắn nhất từ điểm bắt đầu đến điểm kết thúc bằng BFS."""
    if start not in graph or goal not in graph:
        print(f"Lỗi: Điểm bắt đầu '{start}' hoặc điểm kết thúc '{goal}' không có trong đồ thị")
        return None, 0, 0
    visited = set()
    queue = deque([(start, [start])])
    start_time = time.perf_counter()
    while queue:
        vertex, path = queue.popleft()
        if vertex == goal:
            distance = calculate_distance(path, graph)
            return path, time.perf_counter() - start_time, distance
        if vertex not in visited:
            visited.add(vertex)
            for neighbor in graph.get(vertex, {}):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
    return None, time.perf_counter() - start_time, 0

# Thuật toán DFS
def dfs(graph, start, goal):
    """Tìm đường đi từ điểm bắt đầu đến điểm kết thúc bằng DFS."""
    if start not in graph or goal not in graph:
        print(f"Lỗi: Điểm bắt đầu '{start}' hoặc điểm kết thúc '{goal}' không có trong đồ thị")
        return None, 0, 0
    visited = set()
    stack = [(start, [start])]
    start_time = time.perf_counter()
    while stack:
        vertex, path = stack.pop()
        if vertex == goal:
            distance = calculate_distance(path, graph)
            return path, time.perf_counter() - start_time, distance
        if vertex not in visited:
            visited.add(vertex)
            for neighbor in graph.get(vertex, {}):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))
    return None, time.perf_counter() - start_time, 0

# Thuật toán A*
def a_star(graph, start, goal, coordinates):
    if start not in graph or goal not in graph:
        print(f"Lỗi: Điểm bắt đầu '{start}' hoặc điểm kết thúc '{goal}' không có trong đồ thị")
        return None, 0, 0

    def haversine(coord1, coord2):
        lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
        lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        return 6371 * c

    def estimate_coordinates(node, coordinates, graph):
        neighbors = [n for n in graph.get(node, {}) if n in coordinates]
        if neighbors:
            coords = [coordinates[n] for n in neighbors]
            avg_lat = sum(c[0] for c in coords) / len(coords)
            avg_lon = sum(c[1] for c in coords) / len(coords)
            return (avg_lat, avg_lon)
        return coordinates.get(list(coordinates.keys())[0], (0, 0))

    open_set = [(0, start, [start])]
    visited = set()
    g_score = {start: 0}
    start_time = time.perf_counter()

    while open_set:
        f_score, current, path = heappop(open_set)
        if current == goal:
            distance = g_score[current]
            return path, time.perf_counter() - start_time, distance
        if current in visited:
            continue
        visited.add(current)
        for neighbor in graph.get(current, {}):
            if neighbor in visited:
                continue
            tentative_g_score = g_score[current] + graph[current][neighbor]['distance']
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                g_score[neighbor] = tentative_g_score
                h_score = haversine(
                    coordinates.get(neighbor, estimate_coordinates(neighbor, coordinates, graph)),
                    coordinates.get(goal, estimate_coordinates(goal, coordinates, graph))
                )
                f_score = tentative_g_score + h_score
                heappush(open_set, (f_score, neighbor, path + [neighbor]))
    return None, time.perf_counter() - start_time, 0

# Thuật toán Backtracking
def backtracking(graph, start, goal):
    """Tìm đường đi từ điểm bắt đầu đến điểm kết thúc bằng Backtracking."""
    if start not in graph or goal not in graph:
        print(f"Lỗi: Điểm bắt đầu '{start}' hoặc điểm kết thúc '{goal}' không có trong đồ thị")
        return None, 0, 0

    def backtrack(current, goal, visited, path):
        if current == goal:
            return path

        for neighbor in graph.get(current, {}):
            if neighbor not in visited:
                visited.add(neighbor)
                result = backtrack(neighbor, goal, visited, path + [neighbor])
                if result:  # Nếu tìm thấy đường đi
                    return result
                visited.remove(neighbor)  # Quay lui, bỏ neighbor khỏi visited

        return None

    visited = {start}
    start_time = time.perf_counter()
    path = backtrack(start, goal, visited, [start])
    elapsed_time = time.perf_counter() - start_time

    if path:
        distance = calculate_distance(path, graph)
        return path, elapsed_time, distance
    return None, elapsed_time, 0

# Thuật toán Q-learning
def q_learning(graph, start, goal, episodes=1000, alpha=0.1, gamma=0.9, epsilon=0.1):
    """Tìm đường đi từ điểm bắt đầu đến điểm kết thúc bằng Q-learning."""
    if start not in graph or goal not in graph:
        print(f"Lỗi: Điểm bắt đầu '{start}' hoặc điểm kết thúc '{goal}' không có trong đồ thị")
        return None, 0, 0

    # Khởi tạo Q-table
    q_table = {}
    for node in graph:
        q_table[node] = {neighbor: 0 for neighbor in graph[node]}

    start_time = time.perf_counter()

    # Huấn luyện Q-learning
    for _ in range(episodes):
        current_state = start
        while current_state != goal:
            # Chọn hành động (epsilon-greedy)
            if random.uniform(0, 1) < epsilon:
                action = random.choice(list(graph[current_state].keys()))  # Khám phá
            else:
                action = max(q_table[current_state], key=q_table[current_state].get)  # Khai thác

            # Nhận phần thưởng và trạng thái tiếp theo
            next_state = action
            reward = 100 if next_state == goal else -1  # Phần thưởng khi đến đích, phạt mỗi bước

            # Cập nhật Q-value
            current_q = q_table[current_state][action]
            next_max_q = max(q_table[next_state].values()) if next_state in q_table else 0
            q_table[current_state][action] = current_q + alpha * (reward + gamma * next_max_q - current_q)

            current_state = next_state

    # Suy ra đường đi từ Q-table
    path = [start]
    current_state = start
    visited = {start}
    while current_state != goal and current_state in graph:
        next_state = max(q_table[current_state], key=q_table[current_state].get)
        if next_state in visited:
            break  # Tránh vòng lặp
        path.append(next_state)
        visited.add(next_state)
        current_state = next_state

    elapsed_time = time.perf_counter() - start_time

    if path[-1] != goal:
        return None, elapsed_time, 0

    distance = calculate_distance(path, graph)
    return path, elapsed_time, distance

# Thuật toán Incremental Belief-State Search (Sensorless)
def incremental_belief_state_search(graph, goal, initial_belief=None):
    """Tìm chuỗi hành động để đến goal từ bất kỳ trạng thái nào trong initial_belief bằng Incremental Belief-State Search."""
    if goal not in graph:
        print(f"Lỗi: Điểm kết thúc '{goal}' không có trong đồ thị")
        return None, 0, 0

    # Khởi tạo belief state ban đầu
    if initial_belief is None:
        initial_belief = set(graph.keys())
    else:
        initial_belief = set(initial_belief)

    start_time = time.perf_counter()

    def simulate_path(start, path):
        """Mô phỏng đường đi từ một trạng thái theo chuỗi hành động."""
        current = start
        for next_node in path[1:]:
            if current in graph and next_node in graph[current]:
                current = next_node
            else:
                return None
        return current

    def check_path(path, threshold=0.8):
        """Kiểm tra xem đường đi có đưa ít nhất threshold tỷ lệ trạng thái đến goal không."""
        success_count = sum(1 for state in initial_belief if simulate_path(state, path) == goal)
        return success_count / len(initial_belief) >= threshold

    # Tìm tất cả các đường đi từ một trạng thái bất kỳ đến goal
    start_state = next(iter(initial_belief))
    queue = [(0, start_state, [start_state])]  # (chi phí, nút hiện tại, đường đi)
    candidate_paths = []
    visited = {}  # Đếm số lần thăm mỗi nút

    while queue:
        cost, current, path = heappop(queue)
        if current == goal:
            candidate_paths.append(path)
            continue

        visited[current] = visited.get(current, 0) + 1
        if visited[current] > len(graph):
            continue

        for neighbor in graph.get(current, {}):
            new_cost = cost + graph[current][neighbor]['distance']
            heappush(queue, (new_cost, neighbor, path + [neighbor]))

    # Sắp xếp candidate_paths theo chi phí
    candidate_paths.sort(key=lambda p: calculate_distance(p, graph))

    # Kiểm tra tối đa 100 đường đi
    max_paths = 100
    for path in candidate_paths[:max_paths]:
        if check_path(path, threshold=0.8):
            elapsed_time = time.perf_counter() - start_time
            distance = calculate_distance(path, graph)
            return path, elapsed_time, distance

    elapsed_time = time.perf_counter() - start_time
    return None, elapsed_time, 0