import os

def read_distance_file():
    # Lấy đường dẫn tuyệt đối tới file distance.txt
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'distance.txt')

    distance_dict = {}
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) == 3:
                start, end, distance = parts[0], parts[1], float(parts[2])
                if start not in distance_dict:
                    distance_dict[start] = {}
                distance_dict[start][end] = distance
    return distance_dict

'''
---------------------------------
Tao thêm lại 3 cái hàm đọc luôn tại cái trên dùng đường dẫn sẵn t fix hoài không được
---------------------------------'''

def read_abbreviation_file(file_path):
    abbreviations = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, 1):
                line = line.strip()
                if not line or line == "END OF INPUT":
                    continue
                parts = line.split(',', 1)
                if len(parts) != 2:
                    print(f"Lỗi ở dòng {line_number}: Dòng không hợp lệ trong {file_path}: '{line}'")
                    continue
                full_name, code = parts
                full_name = full_name.strip()
                code = code.strip()
                abbreviations[code] = full_name
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file {file_path}")
    return abbreviations

def read_route_file(file_path):
    road_map = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, 1):
                line = line.strip()
                if not line or line == "END OF INPUT":
                    continue
                parts = line.split(',', 2)
                if len(parts) != 3:
                    print(f"Lỗi ở dòng {line_number}: Dòng không hợp lệ trong {file_path}: '{line}' (yêu cầu: src,dest,road_code)")
                    continue
                src, dest, road_code = parts
                src = src.strip()
                dest = dest.strip()
                road_code = road_code.strip()
                if not road_code:
                    print(f"Lỗi ở dòng {line_number}: Mã đường rỗng trong dòng: '{line}'")
                    continue
                road_map.append((src, dest, road_code))
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file {file_path}")
    if not road_map:
        print("Cảnh báo: Không có dữ liệu hợp lệ trong route.txt")
    return road_map

def read_distance_file_blind(file_path):
    edges = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, 1):
                line = line.strip()
                if not line or line == "END OF INPUT":
                    continue
                parts = line.split(',')
                if len(parts) < 3:
                    print(f"Lỗi ở dòng {line_number}: Thiếu cột trong dòng: '{line}' (yêu cầu: src,dest,distance)")
                    continue
                src, dest, distance = parts[:3]
                src = src.strip()
                dest = dest.strip()
                distance = distance.strip()
                try:
                    distance = float(distance)
                except ValueError:
                    print(f"Lỗi ở dòng {line_number}: Khoảng cách không hợp lệ: '{distance}'")
                    continue
                edges.append((src, dest, distance))
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file {file_path}")
    if not edges:
        print("Cảnh báo: Không có dữ liệu hợp lệ trong distance.txt")
    return edges

def PrintDistance(d):
    print(d)

if __name__ == '__main__':
    distances = read_distance_file()
    PrintDistance(distances)