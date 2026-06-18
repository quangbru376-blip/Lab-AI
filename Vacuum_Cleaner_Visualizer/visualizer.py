# visualizer.py
import tkinter as tk
from tkinter import messagebox
import copy
from datetime import datetime

import algorithms 

class VacuumVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Vacuum Cleaner")
        
        self.is_running = False
        self.path_steps = None  
        self.current_step_index = 0
        self.step_counter = 0  
        
        # Khung chứa phần trên
        top_frame = tk.Frame(root)
        top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # PHẦN 1: MÀN HÌNH HIỂN THỊ SÀN
        self.grid_frame = tk.LabelFrame(top_frame, text=f"Màn Hình Hiển Thị Sàn ({algorithms.ROW}x{algorithms.COL})", padx=10, pady=10)
        self.grid_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.labels = [[None for _ in range(algorithms.COL)] for _ in range(algorithms.ROW)]
        for r in range(algorithms.ROW):
            for c in range(algorithms.COL):
                lbl = tk.Label(self.grid_frame, width=8, height=3, font=("Helvetica", 8, "bold"), relief="ridge")
                lbl.grid(row=r, column=c, padx=1, pady=1)
                self.labels[r][c] = lbl

        # Khung dọc bên phải
        right_frame = tk.Frame(top_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        # PHẦN 2: FRAME TÙY CHỌN THUẬT TOÁN (Sử dụng Combobox)
        self.algo_frame = tk.LabelFrame(right_frame, text="Tùy Chọn Thuật Toán", padx=10, pady=10)
        self.algo_frame.pack(fill=tk.X, pady=5)
        
        from tkinter import ttk
        self.algo_combobox = ttk.Combobox(self.algo_frame, state="readonly", width=48)
        self.algo_combobox.pack(fill=tk.X, pady=5)
        
        self.algo_dict = {
            "BFS (Kiểm tra khi sinh con)": "BFS_EARLY",
            "BFS (Kiểm tra chỉ khi lấy từ queue)": "BFS_LATE",
            "DFS (Kiểm tra khi sinh con)": "DFS_EARLY",
            "DFS (Kiểm tra chỉ khi lấy từ stack)": "DFS_LATE",
            "IDS (Kiểm tra khi sinh con)": "IDS_EARLY",
            "IDS (Kiểm tra chỉ khi lấy từ stack)": "IDS_LATE",
            "UCS (Priority Queue - cost ô bẩn)": "UCS",
            "GREEDY (Priority Queue - ít ô bẩn nhất)": "GREEDY",
            "A* (Manhattan + ô bẩn)": "ASTAR",
            "IDA* (Iterative Deepening A*)": "IDA_STAR",
            "Simple Hill Climbing (Leo đồi đơn giản)": "HILL_SIMPLE",
            "Steepest Hill Climbing (Leo đồi dốc nhất)": "HILL_STEEPEST",
            "Stochastic Hill Climbing (Leo đồi ngẫu nhiên)": "HILL_STOCHASTIC",
            "Equal Steepest Hill Climbing (Leo đồi dốc nhất thêm đk bằng)": "HILL_ESTEEPEST",
            "Random Restart Hill Climbing (Leo đồi ngẫu nhiên quay lại)": "HILL_RES_RANDOM",
            "Local Beam Search (Lọc trùng nội bộ - k=2)": "BEAM_LOCAL",
            "Simulated Annealing - Tìm kiếm luyện kim" : "SA",
            "Tìm kiếm AND-OR (Tỉ lệ 20% không di chuyển)" : "AND_OR"
        }
        self.algo_combobox['values'] = list(self.algo_dict.keys())
        self.algo_combobox.current(0)


        # PHẦN 3: CÁC NÚT ĐIỀU KHIỂN
        self.control_frame = tk.LabelFrame(right_frame, text="Điều Khiển", padx=10, pady=10)
        self.control_frame.pack(fill=tk.X, pady=5)
        
        self.btn_run = tk.Button(self.control_frame, text="Chạy", width=10, bg="lightgreen", command=self.start_simulation)
        self.btn_run.pack(side=tk.LEFT, padx=5)
        
        self.btn_stop = tk.Button(self.control_frame, text="Dừng", width=10, bg="lightcoral", command=self.stop_simulation)
        self.btn_stop.pack(side=tk.LEFT, padx=5)
        
        self.btn_reset = tk.Button(self.control_frame, text="Reset", width=10, bg="lightblue", command=self.reset_map)
        self.btn_reset.pack(side=tk.LEFT, padx=5)
        
        # Thêm checkbox chọn sàn cố định
        self.use_fixed_floor = tk.BooleanVar(value=False)
        self.chk_fixed = tk.Checkbutton(self.control_frame, text="Sàn cố định", variable=self.use_fixed_floor, command=self.reset_map)
        self.chk_fixed.pack(side=tk.LEFT, padx=5)

        # PHẦN 4: LOG PANEL (BẢNG TRẠNG THÁI)
        self.log_frame = tk.LabelFrame(root, text="Bảng Trạng Thái Hệ Thống (Log Panel)", padx=10, pady=5)
        self.log_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(self.log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(self.log_frame, height=8, width=65, yscrollcommand=scrollbar.set, font=("Courier", 10))
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.log_text.yview)
        
        self.reset_map()

    def log_message(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)

    def reset_map(self):
        self.is_running = False
        self.path_steps = None  
        self.current_step_index = 0
        self.step_counter = 0
        self.is_and_or_mode = False
        self.tree_plan = None
        self.current_plan_node = None
        
        if hasattr(self, 'use_fixed_floor') and self.use_fixed_floor.get():
            floor, vacuum_pos = algorithms.static_initialize()
        else:
            floor, vacuum_pos = algorithms.floor_and_vacuumpos_initialize()
            
        self.initial_floor = copy.deepcopy(floor)
        self.initial_vacuum_pos = vacuum_pos
        self.current_floor = copy.deepcopy(floor)
        self.current_vacuum_pos = vacuum_pos
        
        if hasattr(self, 'labels'):
            self.update_ui_grid()
            self.log_text.delete("1.0", tk.END)
            self.log_message("Hệ thống đã reset. Hãy chọn thuật toán và bấm nút 'Chạy'.")

    def update_ui_grid(self):
        for r in range(algorithms.ROW):
            for c in range(algorithms.COL):
                lbl = self.labels[r][c]
                if (r, c) == self.current_vacuum_pos:
                    lbl.config(text="🤖 ROBOT", bg="yellow", font=("Helvetica", 7, "bold"))
                elif self.current_floor[r][c] == 1:
                    lbl.config(text="RÁC (1)", bg="#ff9999", font=("Helvetica", 7))
                else:
                    lbl.config(text="SẠCH (0)", bg="#e6e6e6", font=("Helvetica", 7))

    def start_simulation(self):
        if self.is_running:
            return
        
        self.is_running = True
        
        if self.path_steps is None:
            self.current_floor = copy.deepcopy(self.initial_floor)
            self.current_vacuum_pos = self.initial_vacuum_pos
            self.update_ui_grid()
            self.step_counter = 0
            self.current_step_index = 0
            
            selected_name = self.algo_combobox.get()
            algo_choice = self.algo_dict.get(selected_name, "BFS_EARLY")
            self.log_message(f"Khởi động mô phỏng bằng phương pháp: {selected_name}")
            
            # Khởi tạo danh sách các bước đi tương ứng dựa trên thuật toán được chọn
            if algo_choice == "BFS_EARLY":
                self.path_steps = algorithms.run_bfs_early(self.current_floor, self.current_vacuum_pos)
            elif algo_choice == "BFS_LATE":
                self.path_steps = algorithms.run_bfs_late(self.current_floor, self.current_vacuum_pos)
            elif algo_choice == "DFS_EARLY":
                self.path_steps = algorithms.run_dfs_early(self.current_floor, self.current_vacuum_pos)
            elif algo_choice == "DFS_LATE":
                self.path_steps = algorithms.run_dfs_late(self.current_floor, self.current_vacuum_pos)
            elif algo_choice == "IDS_EARLY":
                self.path_steps = algorithms.run_early_iterative_deepening_search(floor= self.current_floor, vacuum_pos= self.current_vacuum_pos)
            elif algo_choice == "IDS_LATE":
                self.path_steps = algorithms.run_late_iterative_deepening_search(floor= self.current_floor, vacuum_pos= self.current_vacuum_pos)
            elif algo_choice == "UCS":
                self.path_steps = algorithms.run_uniform_cost_search(self.current_floor, self.current_vacuum_pos)
            elif algo_choice == "GREEDY":
                self.path_steps = algorithms.run_greedy(self.current_floor, self.current_vacuum_pos)
            elif algo_choice == "ASTAR":
                self.path_steps = algorithms.run_A_Star(self.current_floor, self.current_vacuum_pos)
            elif algo_choice == "IDA_STAR":
                self.path_steps = algorithms.run_ida_star(self.current_floor, self.current_vacuum_pos)
            elif algo_choice == "HILL_SIMPLE":
                self.path_steps = algorithms.run_simple_hill_climbing(self.current_floor, self.current_vacuum_pos)
            elif algo_choice == "HILL_STEEPEST":
                self.path_steps = algorithms.run_steepest_hill_climbing(self.current_floor, self.current_vacuum_pos)
            elif algo_choice == "HILL_STOCHASTIC":
                self.path_steps = algorithms.run_stochastic_hill_climbing(self.current_floor, self.current_vacuum_pos)
            elif algo_choice == "HILL_ESTEEPEST":
                self.path_steps = algorithms.run_equal_steepest_hill_climbing(self.current_floor, self.current_vacuum_pos)
            elif algo_choice == "HILL_RES_RANDOM":
                self.path_steps = algorithms.run_random_restart_hill_climbing(self.current_floor, self.current_vacuum_pos, 10)
            elif algo_choice == "SA":
                self.path_steps = algorithms.run_simulated_annealing(self.current_floor, self.current_vacuum_pos)
            elif algo_choice == "AND_OR":
                self.is_and_or_mode = True
                plan = algorithms.run_and_or(self.current_floor, self.current_vacuum_pos)
                if plan is not None:
                    self.tree_plan = plan
                    self.current_plan_node = plan
                    self.path_steps = True  # Non-None to allow simulation
                    self.log_message("Tìm thấy KẾ HOẠCH DỰ PHÒNG AND-OR:")
                    self.log_message(algorithms.format_plan(plan))
                else:
                    self.is_and_or_mode = False
                    self.tree_plan = None
                    self.current_plan_node = None
                    self.path_steps = None
                    self.is_running = False
                    self.log_message("KẾT THÚC: Không tìm thấy kế hoạch cho bản đồ này.")
                    messagebox.showwarning("Không có lời giải", "Không tìm thấy kế hoạch.")
                    return


        self.run_next_step()

    def stop_simulation(self):
        self.is_running = False
        self.log_message("Đã tạm dừng hành trình.")

    def run_next_step(self):
        if not self.is_running or self.path_steps is None:
            return

        if self.is_and_or_mode:
            import random
            
            # Check goal state
            if self.current_floor == algorithms.GOAL_STATE:
                self.is_running = False
                self.path_steps = None
                self.log_message(f"HOÀN THÀNH: Sàn đã sạch rác hoàn toàn! Tổng số bước: {self.step_counter}")
                messagebox.showinfo("Thành công", "Robot đã hoàn thành đường đi!")
                return
                
            if self.current_plan_node == [] or self.current_plan_node == "LOOP" or self.current_plan_node is None:
                self.is_running = False
                self.path_steps = None
                self.log_message("LỖI: Kế hoạch không hợp lệ.")
                return
                
            action, contingencies = self.current_plan_node
            
            # Simulate 20% slip rate
            roll = random.random()
            if roll < 0.20:
                self.log_message(f"[Bước {self.step_counter}] Hành động: {action} -> TRƯỢT CHÂN (Vẫn ở ô: {self.current_vacuum_pos})")
            else:
                temp_floor, temp_vacuum_pos = algorithms.apply_move(self.current_floor, self.current_vacuum_pos, action)
                self.current_floor = temp_floor
                self.current_vacuum_pos = temp_vacuum_pos
                self.update_ui_grid()
                
                child_state = (tuple(tuple(row) for row in temp_floor), temp_vacuum_pos)
                if child_state not in contingencies:
                    self.is_running = False
                    self.path_steps = None
                    self.log_message(f"LỖI: Trạng thái {child_state} không có trong contingencies!")
                    return
                    
                self.current_plan_node = contingencies[child_state]
                self.log_message(f"[Bước {self.step_counter}] Hành động: {action} -> THÀNH CÔNG (Đến ô: {self.current_vacuum_pos})")
                
            self.step_counter += 1
            
            if self.current_floor == algorithms.GOAL_STATE:
                self.is_running = False
                self.path_steps = None
                self.log_message(f"HOÀN THÀNH: Sàn đã sạch rác hoàn toàn! Tổng số bước: {self.step_counter}")
                messagebox.showinfo("Thành công", "Robot đã hoàn thành đường đi!")
                return
                
            self.root.after(500, self.run_next_step)
            return

        if self.current_step_index >= len(self.path_steps):
            self.is_running = False
            self.path_steps = None
            return

        current_node, is_final_step = self.path_steps[self.current_step_index]
        self.current_step_index += 1
        
        if current_node is None:
            self.is_running = False
            self.path_steps = None
            self.log_message("KẾT THÚC: Không tồn tại đường đi để làm sạch bản đồ này.")
            messagebox.showwarning("Kết thúc", "Không tìm thấy đường đi.")
            return

        self.current_floor = current_node.floor_state
        self.current_vacuum_pos = current_node.position
        self.update_ui_grid()
        
        if self.step_counter == 0:
            self.log_message(f"[Khởi hành] Xuất phát từ ô: {current_node.position}")
        else:
            self.log_message(f"[Bước {self.step_counter}] Hành động: {current_node.birth_action} -> Ô: {current_node.position}")
        
        self.step_counter += 1

        if is_final_step:
            self.is_running = False
            self.path_steps = None
            self.log_message(f"HOÀN THÀNH: Sàn đã sạch rác hoàn toàn! Tổng số bước: {self.step_counter - 1}")
            messagebox.showinfo("Thành công", "Robot đã hoàn thành đường đi!")
            return

        self.root.after(500, self.run_next_step)

if __name__ == "__main__":
    root = tk.Tk()
    app = VacuumVisualizer(root)
    root.mainloop()