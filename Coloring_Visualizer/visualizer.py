import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys
import os

# Import constraints, colors, and the backtracking generator from algorithms.py
try:
    from algorithms import constrains, COLOR, backtracking_coloring_generator
except ImportError:
    # Fallback if algorithms.py is not importable
    constrains = {
        "Thành phố Thủ Đức": ["Quận 1", "Quận 4", "Quận 7", "Quận 12", "Quận Bình Thạnh"],
        "Quận 1": ["Thành phố Thủ Đức", "Quận 3", "Quận 4", "Quận 5", "Quận Bình Thạnh", "Quận Phú Nhuận"],
        "Quận 3": ["Quận 1", "Quận 5", "Quận 10", "Quận Phú Nhuận", "Quận Tân Bình"],
        "Quận 4": ["Thành phố Thủ Đức", "Quận 1", "Quận 5", "Quận 7", "Quận 8"],
        "Quận 5": ["Quận 1", "Quận 3", "Quận 4", "Quận 6", "Quận 8", "Quận 10", "Quận 11"],
        "Quận 6": ["Quận 5", "Quận 8", "Quận 11", "Quận Bình Tân", "Quận Tân Phú"],
        "Quận 7": ["Thành phố Thủ Đức", "Quận 4", "Quận 8", "Huyện Bình Chánh", "Huyện Nhà Bè"],
        "Quận 8": ["Quận 4", "Quận 5", "Quận 6", "Quận 7", "Quận Bình Tân", "Huyện Bình Chánh"],
        "Quận 10": ["Quận 3", "Quận 5", "Quận 11", "Quận Tân Bình"],
        "Quận 11": ["Quận 5", "Quận 6", "Quận 10", "Quận Tân Bình", "Quận Tân Phú"],
        "Quận 12": ["Thành phố Thủ Đức", "Quận Bình Tân", "Quận Gò Vấp", "Quận Bình Thạnh", "Quận Tân Bình", "Huyện Hóc Môn"],
        "Quận Bình Thạnh": ["Thành phố Thủ Đức", "Quận 1", "Quận 12", "Quận Gò Vấp", "Quận Phú Nhuận"],
        "Quận Gò Vấp": ["Quận 12", "Quận Bình Thạnh", "Quận Phú Nhuận", "Quận Tân Bình"],
        "Quận Phú Nhuận": ["Quận 1", "Quận 3", "Quận Bình Thạnh", "Quận Gò Vấp", "Quận Tân Bình"],
        "Quận Tân Bình": ["Quận 3", "Quận 10", "Quận 11", "Quận 12", "Quận Gò Vấp", "Quận Phú Nhuận", "Quận Tân Phú"],
        "Quận Tân Phú": ["Quận 6", "Quận 11", "Quận Tân Bình", "Quận Bình Tân"],
        "Quận Bình Tân": ["Quận 6", "Quận 8", "Quận 12", "Quận Tân Phú", "Huyện Bình Chánh", "Huyện Hóc Môn"],
        "Huyện Bình Chánh": ["Quận 7", "Quận 8", "Quận Bình Tân", "Huyện Hóc Môn", "Huyện Nhà Bè"],
        "Huyện Hóc Môn": ["Quận 12", "Quận Bình Tân", "Huyện Bình Chánh", "Huyện Củ Chi"],
        "Huyện Củ Chi": ["Huyện Hóc Môn"],
        "Huyện Nhà Bè": ["Quận 7", "Huyện Bình Chánh", "Huyện Cần Giờ"],
        "Huyện Cần Giờ": ["Huyện Nhà Bè"]
    }
    COLOR = ["Đỏ", "Cam", "Vàng", "Lục", "Lam", "Đen", "Trắng"]

    def backtracking_coloring_generator(constrains, colors_list, list_of_keys, assignments, idx=0):
        if idx >= len(list_of_keys):
            yield ("SUCCESS", None, None, None)
            return True
        node = list_of_keys[idx]
        for color in colors_list:
            yield ("TRYING", node, color, None)
            conflicts = [nb for nb in constrains[node] if assignments.get(nb) == color]
            if conflicts:
                yield ("CONFLICT", node, color, conflicts)
                continue
            assignments[node] = color
            yield ("ASSIGN", node, color, None)
            sub_gen = backtracking_coloring_generator(constrains, colors_list, list_of_keys, assignments, idx + 1)
            success = False
            while True:
                try:
                    val = next(sub_gen)
                    yield val
                except StopIteration as e:
                    success = e.value
                    break
            if success:
                return True
            assignments[node] = None
            yield ("BACKTRACK", node, color, None)
        return False

# Map Vietnamese color names to Tkinter-compatible hex codes
COLOR_MAP = {
    "Đỏ": "#FF5252",
    "Cam": "#FF9800",
    "Vàng": "#FFEB3B",
    "Lục": "#4CAF50",
    "Lam": "#2196F3",
    "Đen": "#37474F",
    "Trắng": "#FFFFFF"
}

# Geographically-inspired center coordinates for 22 districts (fitting a 700x650 canvas)
COORDS = {
    "Huyện Củ Chi": (150, 70),
    "Huyện Hóc Môn": (220, 150),
    "Quận 12": (310, 200),
    "Quận Gò Vấp": (390, 220),
    "Quận Bình Thạnh": (470, 260),
    "Thành phố Thủ Đức": (590, 230),
    "Quận Phú Nhuận": (410, 280),
    "Quận Tân Bình": (320, 290),
    "Quận Tân Phú": (250, 310),
    "Quận Bình Tân": (180, 320),
    "Huyện Bình Chánh": (130, 440),
    "Quận Tân Bình": (320, 290),
    "Quận Gò Vấp": (390, 220),
    "Quận Phú Nhuận": (410, 280),
    "Quận 3": (390, 340),
    "Quận 10": (340, 350),
    "Quận 11": (290, 360),
    "Quận 6": (240, 400),
    "Quận 5": (330, 400),
    "Quận 1": (440, 340),
    "Quận 4": (460, 400),
    "Quận 8": (320, 460),
    "Quận 7": (500, 460),
    "Huyện Nhà Bè": (510, 540),
    "Huyện Cần Giờ": (590, 600)
}

SHORT_NAMES = {
    "Thành phố Thủ Đức": "Thủ Đức",
    "Quận 1": "Q.1",
    "Quận 3": "Q.3",
    "Quận 4": "Q.4",
    "Quận 5": "Q.5",
    "Quận 6": "Q.6",
    "Quận 7": "Q.7",
    "Quận 8": "Q.8",
    "Quận 10": "Q.10",
    "Quận 11": "Q.11",
    "Quận 12": "Q.12",
    "Quận Bình Thạnh": "Bình Thạnh",
    "Quận Gò Vấp": "Gò Vấp",
    "Quận Phú Nhuận": "Phú Nhuận",
    "Quận Tân Bình": "Tân Bình",
    "Quận Tân Phú": "Tân Phú",
    "Quận Bình Tân": "Bình Tân",
    "Huyện Bình Chánh": "Bình Chánh",
    "Huyện Hóc Môn": "Hóc Môn",
    "Huyện Củ Chi": "Củ Chi",
    "Huyện Nhà Bè": "Nhà Bè",
    "Huyện Cần Giờ": "Cần Giờ"
}

class HCMCMapColoringVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("HCMC Map Coloring Backtracking Visualizer")
        self.root.geometry("1100x700")
        self.root.resizable(True, True)

        # Algorithm state variables
        self.assignments = {district: None for district in constrains.keys()}
        self.list_of_keys = list(constrains.keys())
        self.colors_list = COLOR
        self.generator = None
        self.is_running = False
        self.current_node = None
        self.current_color = None
        self.conflict_nodes = []
        self.step_count = 0
        self.finished = False

        # Build UI
        self.setup_ui()
        self.reset_visualizer()

    def setup_ui(self):
        # Top title frame
        title_frame = tk.Frame(self.root)
        title_frame.pack(fill=tk.X, pady=10)
        
        title_label = tk.Label(
            title_frame, 
            text="Mô phỏng thuật toán tô màu các quận TP. Hồ Chí Minh (Backtracking)", 
            font=("Helvetica", 16, "bold")
        )
        title_label.pack()

        # Main horizontal panel
        main_panel = tk.Frame(self.root)
        main_panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left: Map Canvas
        left_frame = tk.Frame(main_panel)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(left_frame, bg="white", highlightthickness=1)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Right: Sidebar (Controls and Logs)
        right_frame = tk.Frame(main_panel, width=380)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5)
        right_frame.pack_propagate(False)

        # Control Panel frame
        control_frame = tk.LabelFrame(
            right_frame, 
            text="Bảng điều khiển", 
            font=("Helvetica", 11, "bold"), 
            padx=10, 
            pady=10
        )
        control_frame.pack(fill=tk.X, pady=(0, 10))

        # Speed slider
        speed_label = tk.Label(control_frame, text="Tốc độ trễ (ms):", font=("Helvetica", 10))
        speed_label.grid(row=0, column=0, sticky=tk.W, pady=5)

        self.speed_var = tk.IntVar(value=500)
        speed_scale = ttk.Scale(control_frame, from_=100, to=2000, variable=self.speed_var, orient=tk.HORIZONTAL)
        speed_scale.grid(row=0, column=1, columnspan=2, sticky=tk.EW, padx=5, pady=5)
        
        self.speed_display = tk.Label(control_frame, text="500 ms", font=("Helvetica", 10))
        self.speed_display.grid(row=0, column=3, sticky=tk.E, padx=5)
        speed_scale.config(command=self.update_speed_label)

        # Action buttons
        self.btn_auto = tk.Button(
            control_frame, 
            text="Tự động chạy", 
            font=("Helvetica", 10, "bold"), 
            command=self.toggle_auto_run
        )
        self.btn_auto.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW, padx=2, pady=10)

        self.btn_step = tk.Button(
            control_frame, 
            text="Từng bước", 
            font=("Helvetica", 10, "bold"), 
            command=self.trigger_step
        )
        self.btn_step.grid(row=1, column=2, columnspan=2, sticky=tk.NSEW, padx=2, pady=10)

        self.btn_reset = tk.Button(
            control_frame, 
            text="Đặt lại", 
            font=("Helvetica", 10, "bold"), 
            command=self.reset_visualizer
        )
        self.btn_reset.grid(row=2, column=0, columnspan=4, sticky=tk.NSEW, padx=2, pady=5)

        # Status label
        self.status_var = tk.StringVar(value="Đang rảnh. Nhấn Start để chạy.")
        status_label = tk.Label(
            control_frame, 
            textvariable=self.status_var, 
            font=("Helvetica", 10, "italic")
        )
        status_label.grid(row=3, column=0, columnspan=4, pady=5)

        # Color Palette Guide Frame
        palette_frame = tk.LabelFrame(
            right_frame,
            text="Bảng màu khả dụng",
            font=("Helvetica", 11, "bold"),
            padx=10,
            pady=5
        )
        palette_frame.pack(fill=tk.X, pady=(0, 10))

        # Render color circles in palette
        for i, c_name in enumerate(self.colors_list):
            color_hex = COLOR_MAP.get(c_name, "#7F8C8D")
            c_canvas = tk.Canvas(palette_frame, width=20, height=20, highlightthickness=0)
            c_canvas.grid(row=0, column=i*2, padx=(5, 2), pady=5)
            c_canvas.create_oval(2, 2, 18, 18, fill=color_hex, outline="black", width=1)
            
            c_label = tk.Label(palette_frame, text=c_name, font=("Helvetica", 9))
            c_label.grid(row=0, column=i*2+1, padx=(0, 10), pady=5)

        # Log Panel
        log_frame = tk.LabelFrame(
            right_frame, 
            text="Nhật ký hoạt động (Logs)", 
            font=("Helvetica", 11, "bold")
        )
        log_frame.pack(fill=tk.BOTH, expand=True)

        self.log_text = scrolledtext.ScrolledText(
            log_frame, 
            font=("Consolas", 10)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def update_speed_label(self, value):
        self.speed_display.config(text=f"{int(float(value))} ms")

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def draw_map(self):
        self.canvas.delete("all")

        # Draw links (Edges represent adjacent boundaries)
        drawn_edges = set()
        for district, neighbors in constrains.items():
            if district not in COORDS:
                continue
            x1, y1 = COORDS[district]
            for neighbor in neighbors:
                if neighbor not in COORDS:
                    continue
                edge = tuple(sorted([district, neighbor]))
                if edge not in drawn_edges:
                    drawn_edges.add(edge)
                    x2, y2 = COORDS[neighbor]
                    
                    # Highlight edge red if there is a conflict along this edge
                    is_conflict_edge = (
                        self.current_node in (district, neighbor) and 
                        neighbor in self.conflict_nodes or district in self.conflict_nodes
                    )
                    
                    line_color = "#E74C3C" if is_conflict_edge else "#95A5A6"
                    line_width = 3 if is_conflict_edge else 1.5
                    
                    self.canvas.create_line(x1, y1, x2, y2, fill=line_color, width=line_width)

        # Draw nodes (Districts)
        radius = 22
        for district, (x, y) in COORDS.items():
            # Get assigned color
            assigned_color_name = self.assignments[district]
            color_hex = COLOR_MAP.get(assigned_color_name, "#7F8C8D")  # Gray if unassigned
            
            # Border highlight style
            outline_color = "#1ABC9C"  # Smooth teal base border
            outline_width = 1.5
            
            if district == self.current_node:
                outline_color = "#F1C40F"  # Golden outline for currently processing node
                outline_width = 4
            elif district in self.conflict_nodes:
                outline_color = "#E74C3C"  # Red outline for conflict nodes
                outline_width = 4

            # Draw circle representing district
            self.canvas.create_oval(
                x - radius, y - radius, x + radius, y + radius, 
                fill=color_hex, outline=outline_color, width=outline_width
            )

            # Text labels inside node (abbreviation)
            short_name = SHORT_NAMES.get(district, district)
            text_color = "black" if color_hex not in ["#37474F"] else "white"
            self.canvas.create_text(
                x, y, 
                text=short_name, 
                font=("Helvetica", 8, "bold"), 
                fill=text_color
            )
            
            # Text label outside node (full district name, offset slightly above)
            self.canvas.create_text(
                x, y - radius - 8, 
                text=district, 
                font=("Helvetica", 8), 
                fill="black"
            )

    def reset_visualizer(self):
        self.is_running = False
        self.finished = False
        self.btn_auto.config(text="Tự động chạy")
        self.btn_step.config(state=tk.NORMAL)
        
        self.assignments = {district: None for district in constrains.keys()}
        self.generator = self.make_generator()
        self.current_node = None
        self.current_color = None
        self.conflict_nodes = []
        self.step_count = 0
        
        self.status_var.set("Đã đặt lại trạng thái. Nhấn Từng bước hoặc Tự động chạy.")
        self.log_text.delete(1.0, tk.END)
        self.log_message("--- Đã đặt lại bản đồ ---")
        self.draw_map()

    def make_generator(self):
        # Delegate to the backtracking generator imported from algorithms.py
        return backtracking_coloring_generator(
            constrains, 
            self.colors_list, 
            self.list_of_keys, 
            self.assignments
        )

    def run_next_step(self):
        if self.finished or self.generator is None:
            return False

        try:
            action, node, color, extra = next(self.generator)
            self.step_count += 1
            self.current_node = node
            self.current_color = color
            
            if action == "TRYING":
                self.conflict_nodes = []
                self.status_var.set(f"Bước {self.step_count}: Đang kiểm tra màu '{color}' cho {node}...")
                self.log_message(f"- Kiểm tra màu: {node} -> thử màu '{color}'")
                
            elif action == "CONFLICT":
                self.conflict_nodes = extra
                self.status_var.set(f"Bước {self.step_count}: Xung đột! {node} trùng màu với {', '.join(extra)}.")
                self.log_message(f"- Xung đột: {node} trùng màu '{color}' với {', '.join(extra)}")
                
            elif action == "ASSIGN":
                self.conflict_nodes = []
                self.status_var.set(f"Bước {self.step_count}: Gán thành công màu '{color}' cho {node}.")
                self.log_message(f"- Gán màu: {node} -> '{color}'\n")
                
            elif action == "BACKTRACK":
                self.conflict_nodes = []
                self.status_var.set(f"Bước {self.step_count}: Quay lui! Reset màu {node}.")
                self.log_message(f"- Quay lui: {node} không tìm thấy nhánh hợp lệ, hủy màu '{color}'")
                
            elif action == "SUCCESS":
                self.conflict_nodes = []
                self.current_node = None
                self.finished = True
                self.is_running = False
                self.btn_auto.config(text="Hoàn thành", state=tk.DISABLED)
                self.btn_step.config(state=tk.DISABLED)
                self.status_var.set("Hoàn thành! Tìm thấy lời giải tô màu hợp lệ.")
                self.log_message("\nTÌM THẤY LỜI GIẢI HỢP LỆ!")
                for k, v in self.assignments.items():
                    self.log_message(f"   {k:20} -> {v}")
                messagebox.showinfo("Thành công", "Đã tìm thấy phương án tô màu hợp lệ cho bản đồ các quận HCMC!")

            self.draw_map()
            return True

        except StopIteration:
            self.finished = True
            self.is_running = False
            self.btn_auto.config(text="Kết thúc", state=tk.DISABLED)
            self.btn_step.config(state=tk.DISABLED)
            self.status_var.set("Không tìm thấy phương án tô màu khả thi.")
            self.log_message("\nKẾT THÚC: Không tìm thấy phương án tô màu khả thi.")
            messagebox.showwarning("Không có kết quả", "Không tìm thấy lời giải hợp lệ cho danh sách các màu này.")
            return False

    def toggle_auto_run(self):
        if self.finished:
            return

        if self.is_running:
            # Pause
            self.is_running = False
            self.btn_auto.config(text="Tự động chạy")
            self.status_var.set("Đã tạm dừng mô phỏng.")
        else:
            # Start/Resume
            self.is_running = True
            self.btn_auto.config(text="Tạm dừng")
            self.status_var.set("Đang tự động chạy...")
            self.auto_run_loop()

    def auto_run_loop(self):
        if not self.is_running or self.finished:
            return

        if self.run_next_step():
            delay = self.speed_var.get()
            self.root.after(delay, self.auto_run_loop)

    def trigger_step(self):
        if self.is_running:
            self.toggle_auto_run()  # Pause auto run first if running
        self.run_next_step()

def main():
    root = tk.Tk()
    app = HCMCMapColoringVisualizer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
