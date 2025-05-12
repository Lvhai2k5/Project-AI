import tkinter as tk
from tkinter import ttk
import tkintermapview
from ReadFile import read_distance_file
from ucs import UniformCostSearch
from genetic_algorithm import GeneticAlgorithm
from algorithm import bfs, dfs, a_star, backtracking, q_learning, incremental_belief_state_search, abbreviations, graph, simplify_path

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Bản đồ các trường Thủ Đức')
        self.state('zoomed')

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        route_file = 'route.txt'
        abbreviation_file = 'abbreviation.txt'
        # Load distances
        self.distances = read_distance_file()

        self.ucs_solver = UniformCostSearch(self.distances)
        self.ga_solver = GeneticAlgorithm(self.distances, population_size=100, generations=200, mutation_rate=0.1)

        self.coordinates = {
            'HCMUTE': (10.849907, 106.773420),  # ĐH Sư phạm Kỹ thuật TP.HCM
            'UEL': (10.87019181520931, 106.778135514584),  # ĐH Kinh tế - Luật
            'UIT': (10.870124940842583, 106.80305894475933),  # ĐH Công nghệ Thông tin TP.HCM
            'HCMUSSH': (10.873458, 106.802335),  # ĐH Khoa học Xã hội và Nhân văn TP.HCM
            'HCMUS': (10.875539562515387, 106.79967895243253),  # ĐH Khoa học Tự nhiên TP.HCM
            'ANND': (10.873631584605281, 106.80433580470206),  # ĐH An ninh Nhân dân
            'IU': (10.8777316065133, 106.80163682829702),  # ĐH Quốc tế
            'NLU': (10.867922, 106.787755),  # ĐH Nông Lâm TP.HCM
            'FPT': (10.841412097704094, 106.80990445407129),  # ĐH FPT TP.HCM
            'VMTTN': (10.879819188943543, 106.78716817858859),  # Viện Môi trường và Tài nguyên
            'HUB': (10.857551375222272, 106.76359717190293),  # ĐH Ngân hàng TP.HCM
            'UTH': (10.845230906011794, 106.79394555464994),  # ĐH Giao thông Vận tải TP.HCM
            'HUTECH': (10.856022683787254, 106.78563898290743),  # ĐH Công nghệ TP.HCM
            'UAH': (10.841907522562371, 106.76441304243153),  # ĐH Kiến trúc TP.HCM
            'HCMUC': (10.823689976583585, 106.77014711544741),  # ĐH Văn hóa TP.HCM
            'BKU': (10.880789000711756, 106.80541593161053),  # ĐH Bách Khoa TP.HCM
            'GHD2LVC': (10.854416, 106.772974),  # Giao Hoàng Diệu 2 và Lê Văn Chí
            'GLVCQL1K': (10.867681, 106.781995),  # Giao Lê Văn Chí và Quốc lộ 1K
            'GD14LT': (10.860811, 106.771737),  # Giao Đường 14 và Linh Trung
            'GLTLVC': (10.858938, 106.777844),  # Giao Linh Trung và Lê Văn Chí
            'GD6HD2': (10.857361, 106.763858),  # Giao Đường 6 và Hoàng Diệu 2
            'GSHD1': (10.857951, 106.787832),  # Giao Song Hành và D1
            'GDVDLVV': (10.848978, 106.808708),  # Giao Đường Vành Đai và Lê Văn Việt
            'GSHD400': (10.871950, 106.807946),  # Giao Song Hành và Đường 400
            'GLVVD385': (10.844417, 106.789787),  # Giao Lê Văn Việt và Đường 385
            'CDLVV': (10.850213, 106.813704),  # Cuối Đường Lê Văn Việt
            'GHHND400': (10.870202, 106.814069),  # Giao Nguyễn Văn Bá và Đường 400
            'GNVBDVB': (10.838228, 106.766879),  # Giao Nguyễn Văn Bá và Đặng Văn Bi
            'GNVBDXH': (10.835772, 106.765571),  # Giao Nguyễn Văn Bá và Đỗ Xuân Hợp
            'GDXHDDH': (10.816724, 106.774246),  # Giao Đỗ Xuân Hợp và Dương Đình Hội
            'GDDHDPP': (10.830642, 106.783416),  # Giao Dương Đình Hội và Đình Phong Phú
            'GDPPLVV': (10.844472, 106.781262),  # Giao Đình Phong Phú và Lê Văn Việt
            'GSHDLDH': (10.873096, 106.808481),  # Giao Song Hành và Đại Lộ Đại Học
            'GSHO1': (10.871112, 106.806492),  # Giao Song Hành và Overpass 01
            'GDLDHQTST': (10.875121, 106.805294),  # Giao Đại Lộ Đại Học và Quảng Trường Sáng Tạo
            'GQTSTTQB': (10.876110, 106.804603),  # Giao Quảng Trường Sáng Tạo và Tạ Quang Bửu
            'N4LQ': (10.878670, 106.802446),  # Ngã 4 tượng nhà bác học Lê Quý Đôn
            'GQTSTLQD': (10.876489, 106.803196),  # Giao Quảng Trường Sáng Tạo và Lê Quý Đôn
            'GQTSTWS': (10.876363, 106.800760),  # Giao Quảng Trường Sáng Tạo và William Shakespeare
            'GLQDND': (10.883244, 106.800650),  # Giao Lê Quý Đôn và Nguyễn Du
            'GWSND': (10.881079, 106.796591),  # Giao William Shakespeare và Nguyễn Du
            'KTXB': (10.882050, 106.782637),  # Ký Túc Xá Khu B ĐHQG
            'GMDCD2': (10.875050, 106.778335),  # Giao Mạc Đĩnh Chi và Đường Số 2
            'GDD12B': (10.839290, 106.811711),  # Giao D1 và 2B
            'GD2BVD': (10.842940, 106.815240)  # Giao 2B và Vành Đai
        }
        self.universities = list(self.coordinates.keys())

        # Right menu frame
        self.lbl_menu = tk.LabelFrame(self, text='Menu', width=400, height=400)
        self.lbl_menu.grid(row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)
        self.lbl_menu.grid_propagate(False)

        self.notebook = ttk.Notebook(self.lbl_menu)

        # Tab 1: Đường đi ngắn nhất (UCS)
        self.tab_1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_1, text='Đường đi ngắn nhất')

        # Tab 2: Đi qua nhiều trường (Genetic Algorithm)
        self.tab_2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_2, text='Đi qua nhiều trường')

        # Tab 3: Làm với thuật toán mù
        self.tab_3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_3, text='Đường đi ngẫu nhiên')

        self.notebook.grid(row=0, column=0, padx=5, pady=7, sticky=tk.EW)

        # Tab 1: Giao diện
        lbl_bat_dau_1 = ttk.Label(self.tab_1, text='Điểm bắt đầu:')
        lbl_bat_dau_1.grid(row=0, column=0, padx=5, pady=10, sticky=tk.W)
        self.cbo_bat_dau_1 = ttk.Combobox(self.tab_1, values=self.universities, width=20)
        self.cbo_bat_dau_1.set('Chọn trường')
        self.cbo_bat_dau_1.grid(row=0, column=1, padx=5, pady=10, sticky=tk.EW)

        lbl_ket_thuc_1 = ttk.Label(self.tab_1, text='Điểm kết thúc:')
        lbl_ket_thuc_1.grid(row=1, column=0, padx=5, pady=10, sticky=tk.W)
        self.cbo_ket_thuc_1 = ttk.Combobox(self.tab_1, values=self.universities, width=20)
        self.cbo_ket_thuc_1.set('Chọn trường')
        self.cbo_ket_thuc_1.grid(row=1, column=1, padx=5, pady=10, sticky=tk.EW)

        btn_tim_duong_1 = ttk.Button(self.tab_1, text='Tìm đường đi', command=self.find_path_ucs)
        btn_tim_duong_1.grid(row=2, column=0, columnspan=2, padx=5, pady=20, sticky=tk.EW)

        # Tab 2: Giao diện
        lbl_bat_dau_2 = ttk.Label(self.tab_2, text='Điểm bắt đầu:')
        lbl_bat_dau_2.grid(row=0, column=0, padx=5, pady=10, sticky=tk.W)
        self.cbo_bat_dau_2 = ttk.Combobox(self.tab_2, values=self.universities, width=20)
        self.cbo_bat_dau_2.set('Chọn trường')
        self.cbo_bat_dau_2.grid(row=0, column=1, padx=5, pady=10, sticky=tk.EW)

        lbl_ket_thuc_2 = ttk.Label(self.tab_2, text='Điểm kết thúc:')
        lbl_ket_thuc_2.grid(row=1, column=0, padx=5, pady=10, sticky=tk.W)
        self.cbo_ket_thuc_2 = ttk.Combobox(self.tab_2, values=self.universities + ['Không'], width=20)
        self.cbo_ket_thuc_2.set('Không')
        self.cbo_ket_thuc_2.grid(row=1, column=1, padx=5, pady=10, sticky=tk.EW)

        lbl_stops = ttk.Label(self.tab_2, text='Trạm trung gian:')
        lbl_stops.grid(row=2, column=0, padx=5, pady=10, sticky=tk.W)
        self.listbox_stops = tk.Listbox(self.tab_2, selectmode=tk.MULTIPLE, height=6, width=20)
        for uni in self.universities:
            self.listbox_stops.insert(tk.END, uni)
        self.listbox_stops.grid(row=2, column=1, padx=5, pady=10, sticky=tk.EW)

        btn_tim_duong_2 = ttk.Button(self.tab_2, text='Tìm đường đi', command=self.find_path_ga)
        btn_tim_duong_2.grid(row=3, column=0, columnspan=2, padx=5, pady=20, sticky=tk.EW)

        # Tab 3: Giao diện
        lbl_bat_dau_3 = ttk.Label(self.tab_3, text='Điểm bắt đầu:')
        lbl_bat_dau_3.grid(row=0, column=0, padx=5, pady=10, sticky=tk.W)
        self.cbo_bat_dau_3 = ttk.Combobox(self.tab_3, values=self.universities, width=20)
        self.cbo_bat_dau_3.set('Chọn trường')
        self.cbo_bat_dau_3.grid(row=0, column=1, padx=5, pady=10, sticky=tk.EW)

        lbl_ket_thuc_3 = ttk.Label(self.tab_3, text='Điểm kết thúc:')
        lbl_ket_thuc_3.grid(row=1, column=0, padx=5, pady=10, sticky=tk.W)
        self.cbo_ket_thuc_3 = ttk.Combobox(self.tab_3, values=self.universities, width=20)
        self.cbo_ket_thuc_3.set('Chọn trường')
        self.cbo_ket_thuc_3.grid(row=1, column=1, padx=5, pady=10, sticky=tk.EW)

        lbl_belief = ttk.Label(self.tab_3, text='Trạng thái ban đầu (Belief State):')
        lbl_belief.grid(row=2, column=0, padx=5, pady=10, sticky=tk.W)
        self.listbox_belief = tk.Listbox(self.tab_3, selectmode=tk.MULTIPLE, height=6, width=20)
        for uni in self.universities:
            self.listbox_belief.insert(tk.END, uni)
        self.listbox_belief.grid(row=2, column=1, padx=5, pady=10, sticky=tk.EW)

        btn_tim_duong_3 = ttk.Button(self.tab_3, text='Tìm đường đi', command=self.find_path_blind)
        btn_tim_duong_3.grid(row=3, column=0, columnspan=2, padx=5, pady=20, sticky=tk.EW)

        # Result frame
        self.lbl_result = tk.LabelFrame(self, text='Kết quả', height=400, width=400)
        self.lbl_result.grid(row=1, column=1, padx=10, pady=10, sticky=tk.NSEW)
        self.lbl_result.grid_propagate(False)
        self.textketqua = tk.Text(self.lbl_result, width=47, height=22)
        self.textketqua.tag_configure('center', justify='center', font=('Georgia', 12))
        self.textketqua.tag_configure('bold', font=('Georgia', 12, 'bold'))
        self.textketqua.tag_configure('normal', font=('Georgia', 12))
        self.textketqua.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

        # Map
        self.map_widget = tkintermapview.TkinterMapView(self, width=800, height=600, corner_radius=0)
        self.map_widget.grid(row=0, column=0, rowspan=2, padx=5, pady=5, sticky=tk.NSEW)
        self.map_widget.set_position(10.849907, 106.773420)
        self.map_widget.set_zoom(14)

        # Add markers
        self.markers = {}
        for uni in self.universities:
            lat, lon = self.coordinates[uni]
            self.markers[uni] = self.map_widget.set_marker(lat, lon, text=uni, marker_color_circle="gray")

    def interpolate_points(self, start_coord, end_coord, num_points=5):
        """Tạo các điểm trung gian để vẽ đường đi mượt mà hơn."""
        lat1, lon1 = start_coord
        lat2, lon2 = end_coord
        points = []
        for i in range(num_points + 1):
            t = i / num_points
            lat = lat1 + t * (lat2 - lat1)
            lon = lon1 + t * (lon2 - lon1)
            points.append((lat, lon))
        return points

    def display_path(self, path, total_distance, start, end, stops=None):
        """Hiển thị đường đi trên giao diện văn bản và bản đồ."""
        self.textketqua.delete("1.0", tk.END)
        self.map_widget.delete_all_path()

        # Hiển thị kết quả văn bản
        self.textketqua.insert(tk.END, f"Đường đi từ {abbreviations.get(start, start)}", 'bold')
        if stops:
            self.textketqua.insert(tk.END, f" qua {', '.join(abbreviations.get(s, s) for s in stops)}", 'normal')
        if end:
            self.textketqua.insert(tk.END, f" đến {abbreviations.get(end, end)}", 'bold')
        self.textketqua.insert(tk.END, ":\n", 'normal')

        if not path:
            self.textketqua.insert(tk.END, "Không tìm thấy đường đi hợp lệ!\n", 'normal')
            return

        # Gộp đường đi để hiển thị ngắn gọn
        simplified_path = simplify_path(path, graph)
        for seg_start, seg_end, road in simplified_path:
            seg_start_display = abbreviations.get(seg_start, seg_start)
            seg_end_display = abbreviations.get(seg_end, seg_end)
            if road:
                self.textketqua.insert(tk.END,
                                       f"  - Đi từ {seg_start_display} đến {seg_end_display} trên đường {road}\n",
                                       'normal')
            else:
                self.textketqua.insert(tk.END, f"  - Đi từ {seg_start_display} đến {seg_end_display}\n", 'normal')
        self.textketqua.insert(tk.END, f"\nTổng khoảng cách: {total_distance:.2f} km\n", 'bold')

        # Vẽ đường đi trên bản đồ
        path_coords = [self.coordinates[node] for node in path if node in self.coordinates]
        if len(path_coords) >= 2:
            self.map_widget.set_path(path_coords, color="red", width=3)
        else:
            self.textketqua.insert(tk.END, "Không thể vẽ đường đi: Không đủ tọa độ!\n", 'normal')

        # Cập nhật màu sắc cho các điểm
        for uni in self.markers:
            self.markers[uni].delete()
            color = "gray"
            if uni == start:
                color = "green"
            elif end and uni == end:
                color = "red"
            elif stops and uni in stops:
                color = "blue"
            lat, lon = self.coordinates[uni]
            self.markers[uni] = self.map_widget.set_marker(lat, lon, text=uni, marker_color_circle=color)

    def find_path_ucs(self):
        """Tìm đường đi ngắn nhất bằng UCS."""
        start = self.cbo_bat_dau_1.get()
        end = self.cbo_ket_thuc_1.get()

        if start not in self.universities:
            self.textketqua.delete("1.0", tk.END)
            self.textketqua.insert(tk.END, "Vui lòng chọn điểm bắt đầu hợp lệ!\n", 'bold')
            return

        if end not in self.universities:
            self.textketqua.delete("1.0", tk.END)
            self.textketqua.insert(tk.END, "Vui lòng chọn điểm kết thúc hợp lệ!\n", 'bold')
            return

        if start == end:
            self.textketqua.delete("1.0", tk.END)
            self.textketqua.insert(tk.END, "Điểm bắt đầu và kết thúc không được trùng nhau!\n", 'bold')
            return

        path, total_distance = self.ucs_solver.find_path(start, end)
        if not path or total_distance == float('infinity'):
            self.textketqua.delete("1.0", tk.END)
            self.textketqua.insert(tk.END, "Không tìm thấy đường đi! Các điểm không liên thông.\n", 'bold')
            return

        self.display_path(path, total_distance, start, end)

    def find_path_ga(self):
        """Tìm đường đi qua nhiều điểm bằng Genetic Algorithm."""
        start = self.cbo_bat_dau_2.get()
        end = self.cbo_ket_thuc_2.get()
        stops = [self.listbox_stops.get(i) for i in self.listbox_stops.curselection()]

        if start not in self.universities:
            self.textketqua.delete("1.0", tk.END)
            self.textketqua.insert(tk.END, "Vui lòng chọn điểm bắt đầu hợp lệ!\n", 'bold')
            return

        if end == 'Không':
            end = None
        elif end not in self.universities:
            self.textketqua.delete("1.0", tk.END)
            self.textketqua.insert(tk.END, "Vui lòng chọn điểm kết thúc hợp lệ!\n", 'bold')
            return

        if not stops and not end:
            self.textketqua.delete("1.0", tk.END)
            self.textketqua.insert(tk.END, "Vui lòng chọn ít nhất một trạm trung gian hoặc điểm kết thúc!\n", 'bold')
            return

        if end and end in stops:
            self.textketqua.delete("1.0", tk.END)
            self.textketqua.insert(tk.END, "Điểm kết thúc không được trùng với trạm trung gian!\n", 'bold')
            return

        if start in stops:
            self.textketqua.delete("1.0", tk.END)
            self.textketqua.insert(tk.END, "Điểm bắt đầu không được trùng với trạm trung gian!\n", 'bold')
            return

        path, total_distance = self.ga_solver.find_path(start, stops, end)
        if not path or total_distance >= 1e6:  # Giá trị phạt lớn từ GA
            self.textketqua.delete("1.0", tk.END)
            self.textketqua.insert(tk.END, "Không tìm thấy đường đi qua các trạm! Kiểm tra tính liên thông.\n", 'bold')
            return

        self.display_path(path, total_distance, start, end, stops)

    def find_path_blind(self):
        """Tìm đường đi bằng các thuật toán mù, A*, và Sensorless."""
        self.textketqua.delete("1.0", tk.END)
        self.map_widget.delete_all_path()

        start = self.cbo_bat_dau_3.get()
        end = self.cbo_ket_thuc_3.get()
        initial_belief = [self.listbox_belief.get(i) for i in self.listbox_belief.curselection()]

        if start not in self.universities:
            self.textketqua.insert(tk.END, "Vui lòng chọn điểm bắt đầu hợp lệ!\n", 'bold')
            return

        if end not in self.universities:
            self.textketqua.insert(tk.END, "Vui lòng chọn điểm kết thúc hợp lệ!\n", 'bold')
            return

        if start == end:
            self.textketqua.insert(tk.END, "Vui lòng chọn điểm xuất phát và đích khác nhau!\n", 'bold')
            return

        if not initial_belief:
            initial_belief = [uni for uni in self.universities if uni != end]  # Mặc định nếu không chọn
        if end in initial_belief:
            self.textketqua.insert(tk.END, "Điểm kết thúc không được nằm trong Belief State!\n", 'bold')
            return

        # Kiểm tra tính khả thi của initial_belief
        for state in initial_belief:
            path, _, _ = bfs(graph, state, end)
            if not path:
                self.textketqua.insert(tk.END, f"Không có đường đi từ {abbreviations.get(state, state)} đến {abbreviations.get(end, end)}!\n", 'bold')
                return

        # Chạy BFS
        bfs_path, bfs_time, bfs_distance = bfs(graph, start, end)
        print("BFS path:", bfs_path, "Distance:", bfs_distance)

        # Chạy DFS
        dfs_path, dfs_time, dfs_distance = dfs(graph, start, end)
        print("DFS path:", dfs_path, "Distance:", dfs_distance)

        # Chạy A*
        a_star_path, a_star_time, a_star_distance = a_star(graph, start, end, self.coordinates)
        print("A* path:", a_star_path, "Distance:", a_star_distance)

        # Chạy Backtracking
        backtracking_path, backtracking_time, backtracking_distance = backtracking(graph, start, end)
        print("Backtracking path:", backtracking_path, "Distance:", backtracking_distance)

        # Chạy Q-learning
        q_learning_path, q_learning_time, q_learning_distance = q_learning(graph, start, end)
        print("Q-learning path:", q_learning_path, "Distance:", q_learning_distance)

        # Chạy Sensorless
        sensorless_path, sensorless_time, sensorless_distance = incremental_belief_state_search(
            graph, end, initial_belief
        )
        print("Sensorless path:", sensorless_path, "Distance:", sensorless_distance)

        # Hiển thị kết quả
        self.textketqua.insert(tk.END, "Kết quả so sánh BFS, DFS, A*, Backtracking, Q-learning và Sensorless:\n", 'bold')

        # Hiển thị BFS
        self.textketqua.insert(tk.END, "\nBFS:\n", 'bold')
        if bfs_path:
            self.textketqua.insert(tk.END,
                                   f"Từ {abbreviations.get(start, start)} ---> {abbreviations.get(end, end)}:\n",
                                   'bold')
            simplified_path = simplify_path(bfs_path, graph)
            for seg_start, seg_end, road in simplified_path:
                seg_start_display = abbreviations.get(seg_start, seg_start)
                seg_end_display = abbreviations.get(seg_end, seg_end)
                if road:
                    self.textketqua.insert(tk.END,
                                           f"  - Đi từ {seg_start_display} đến {seg_end_display} trên đường {road}\n",
                                           'normal')
                else:
                    self.textketqua.insert(tk.END, f"  - Đi từ {seg_start_display} ---> {seg_end_display}\n", 'normal')
            self.textketqua.insert(tk.END, f"\nTổng khoảng cách: {bfs_distance:.2f} km\n", 'normal')
            self.textketqua.insert(tk.END, f"Thời gian chạy thuật toán: {bfs_time:.6f} giây\n", 'normal')
        else:
            self.textketqua.insert(tk.END, "Không tìm thấy đường đi!\n", 'normal')

        # Hiển thị DFS
        self.textketqua.insert(tk.END, "\nDFS:\n", 'bold')
        if dfs_path:
            self.textketqua.insert(tk.END,
                                   f"Từ {abbreviations.get(start, start)} ---> {abbreviations.get(end, end)}:\n",
                                   'bold')
            simplified_path = simplify_path(dfs_path, graph)
            for seg_start, seg_end, road in simplified_path:
                seg_start_display = abbreviations.get(seg_start, seg_start)
                seg_end_display = abbreviations.get(seg_end, seg_end)
                if road:
                    self.textketqua.insert(tk.END,
                                           f"  - Đi từ {seg_start_display} đến {seg_end_display} trên đường {road}\n",
                                           'normal')
                else:
                    self.textketqua.insert(tk.END, f"  - Đi từ {seg_start_display} ---> {seg_end_display}\n", 'normal')
            self.textketqua.insert(tk.END, f"\nTổng khoảng cách: {dfs_distance:.2f} km\n", 'normal')
            self.textketqua.insert(tk.END, f"Thời gian chạy thuật toán: {dfs_time:.6f} giây\n", 'normal')
        else:
            self.textketqua.insert(tk.END, "Không tìm thấy đường đi!\n", 'normal')

        # Hiển thị A*
        self.textketqua.insert(tk.END, "\nA*:\n", 'bold')
        if a_star_path:
            self.textketqua.insert(tk.END,
                                   f"Từ {abbreviations.get(start, start)} ---> {abbreviations.get(end, end)}:\n",
                                   'bold')
            simplified_path = simplify_path(a_star_path, graph)
            for seg_start, seg_end, road in simplified_path:
                seg_start_display = abbreviations.get(seg_start, seg_start)
                seg_end_display = abbreviations.get(seg_end, seg_end)
                if road:
                    self.textketqua.insert(tk.END,
                                           f"  - Đi từ {seg_start_display} đến {seg_end_display} trên đường {road}\n",
                                           'normal')
                else:
                    self.textketqua.insert(tk.END, f"  - Đi từ {seg_start_display} ---> {seg_end_display}\n", 'normal')
            self.textketqua.insert(tk.END, f"\nTổng khoảng cách: {a_star_distance:.2f} km\n", 'normal')
            self.textketqua.insert(tk.END, f"Thời gian chạy thuật toán: {a_star_time:.6f} giây\n", 'normal')
        else:
            self.textketqua.insert(tk.END, "Không tìm thấy đường đi!\n", 'normal')

        # Hiển thị Backtracking
        self.textketqua.insert(tk.END, "\nBacktracking:\n", 'bold')
        if backtracking_path:
            self.textketqua.insert(tk.END,
                                   f"Từ {abbreviations.get(start, start)} ---> {abbreviations.get(end, end)}:\n",
                                   'bold')
            simplified_path = simplify_path(backtracking_path, graph)
            for seg_start, seg_end, road in simplified_path:
                seg_start_display = abbreviations.get(seg_start, seg_start)
                seg_end_display = abbreviations.get(seg_end, seg_end)
                if road:
                    self.textketqua.insert(tk.END,
                                           f"  - Đi từ {seg_start_display} đến {seg_end_display} trên đường {road}\n",
                                           'normal')
                else:
                    self.textketqua.insert(tk.END, f"  - Đi từ {seg_start_display} ---> {seg_end_display}\n", 'normal')
            self.textketqua.insert(tk.END, f"\nTổng khoảng cách: {backtracking_distance:.2f} km\n", 'normal')
            self.textketqua.insert(tk.END, f"Thời gian chạy thuật toán: {backtracking_time:.6f} giây\n", 'normal')
        else:
            self.textketqua.insert(tk.END, "Không tìm thấy đường đi!\n", 'normal')

        # Hiển thị Q-learning
        self.textketqua.insert(tk.END, "\nQ-learning:\n", 'bold')
        if q_learning_path:
            self.textketqua.insert(tk.END,
                                   f"Từ {abbreviations.get(start, start)} ---> {abbreviations.get(end, end)}:\n",
                                   'bold')
            simplified_path = simplify_path(q_learning_path, graph)
            for seg_start, seg_end, road in simplified_path:
                seg_start_display = abbreviations.get(seg_start, seg_start)
                seg_end_display = abbreviations.get(seg_end, seg_end)
                if road:
                    self.textketqua.insert(tk.END,
                                           f"  - Đi từ {seg_start_display} đến {seg_end_display} trên đường {road}\n",
                                           'normal')
                else:
                    self.textketqua.insert(tk.END, f"  - Đi từ {seg_start_display} ---> {seg_end_display}\n", 'normal')
            self.textketqua.insert(tk.END, f"\nTổng khoảng cách: {q_learning_distance:.2f} km\n", 'normal')
            self.textketqua.insert(tk.END, f"Thời gian chạy thuật toán: {q_learning_time:.6f} giây\n", 'normal')
        else:
            self.textketqua.insert(tk.END, "Không tìm thấy đường đi!\n", 'normal')

        # Hiển thị Sensorless
        self.textketqua.insert(tk.END, "\nSensorless (Belief-State Search):\n", 'bold')
        if sensorless_path:
            self.textketqua.insert(tk.END,
                                   f"Đường đi cố định đến {abbreviations.get(end, end)} từ các điểm trong belief state:\n",
                                   'bold')
            simplified_path = simplify_path(sensorless_path, graph)
            for seg_start, seg_end, road in simplified_path:
                seg_start_display = abbreviations.get(seg_start, seg_start)
                seg_end_display = abbreviations.get(seg_end, seg_end)
                if road:
                    self.textketqua.insert(tk.END,
                                           f"  - Đi từ {seg_start_display} đến {seg_end_display} trên đường {road}\n",
                                           'normal')
                else:
                    self.textketqua.insert(tk.END, f"  - Đi từ {seg_start_display} ---> {seg_end_display}\n", 'normal')
            self.textketqua.insert(tk.END, f"\nTổng khoảng cách: {sensorless_distance:.2f} km\n", 'normal')
            self.textketqua.insert(tk.END, f"Thời gian chạy thuật toán: {sensorless_time:.6f} giây\n", 'normal')
        else:
            self.textketqua.insert(tk.END, "Không tìm thấy đường đi cố định!\n", 'normal')

        # Vẽ đường đi trên bản đồ
        if bfs_path:
            bfs_coords = [self.coordinates[node] for node in bfs_path if node in self.coordinates]
            print("BFS coords:", bfs_coords)
            if len(bfs_coords) > 1:
                self.map_widget.set_path(bfs_coords, color="blue", width=3)
        if dfs_path:
            dfs_coords = [self.coordinates[node] for node in dfs_path if node in self.coordinates]
            print("DFS coords:", dfs_coords)
            if len(dfs_coords) > 1:
                self.map_widget.set_path(dfs_coords, color="red", width=3)
        if a_star_path:
            a_star_coords = [self.coordinates[node] for node in a_star_path if node in self.coordinates]
            print("A* coords:", a_star_coords)
            if len(a_star_coords) > 1:
                self.map_widget.set_path(a_star_coords, color="green", width=3)
        if backtracking_path:
            backtracking_coords = [self.coordinates[node] for node in backtracking_path if node in self.coordinates]
            print("Backtracking coords:", backtracking_coords)
            if len(backtracking_coords) > 1:
                self.map_widget.set_path(backtracking_coords, color="purple", width=3)
        if q_learning_path:
            q_learning_coords = [self.coordinates[node] for node in q_learning_path if node in self.coordinates]
            print("Q-learning coords:", q_learning_coords)
            if len(q_learning_coords) > 1:
                self.map_widget.set_path(q_learning_coords, color="yellow", width=3)
        if sensorless_path:
            sensorless_coords = [self.coordinates[node] for node in sensorless_path if node in self.coordinates]
            print("Sensorless coords:", sensorless_coords)
            if len(sensorless_coords) > 1:
                self.map_widget.set_path(sensorless_coords, color="orange", width=3)

        # Cập nhật marker
        for marker in self.markers.values():
            marker.delete()
        self.markers.clear()
        for uni in self.universities:
            if uni in self.coordinates:
                lat, lon = self.coordinates[uni]
                color = "gray"
                if uni == start:
                    color = "green"
                elif uni == end:
                    color = "red"
                self.markers[uni] = self.map_widget.set_marker(lat, lon, text=uni, marker_color_circle=color)

def main():
    """Hàm main để khởi chạy ứng dụng."""
    app = App()
    app.mainloop()

if __name__ == '__main__':
    main()