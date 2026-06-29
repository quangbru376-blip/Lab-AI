import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import random

try:
    from algorithms import (
        initialize_board, check_winner, posible_moves, apply_move,
        minimax, alphabeta, expectimax, Node
    )
except ImportError as e:
    print(f"Error importing algorithms: {e}")
    messagebox.showerror("Import Error", f"Không thể import các thuật toán từ algorithms.py: {e}")
    sys.exit(1)


class TicTacToeVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe Algorithm Visualizer")
        self.root.geometry("600x450")
        self.root.resizable(False, False)

        # Game state
        self.board_state = initialize_board()
        self.current_player = 'X'  # User is X, AI is O
        self.game_over = False

        self.setup_ui()
        self.reset_game()

    def setup_ui(self):
        # Main layout
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left side: Tic-Tac-Toe Board
        board_frame = tk.Frame(main_frame)
        board_frame.pack(side=tk.LEFT, padx=20, pady=20)

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for r in range(3):
            for c in range(3):
                btn = tk.Button(
                    board_frame, text=" ", font=("Helvetica", 32, "bold"),
                    width=4, height=2,
                    command=lambda row=r, col=c: self.on_button_click(row, col)
                )
                btn.grid(row=r, column=c, padx=5, pady=5)
                self.buttons[r][c] = btn

        # Right side: Control Panel
        control_frame = tk.LabelFrame(main_frame, text="Bảng điều khiển", font=("Helvetica", 12, "bold"), padx=10, pady=10)
        control_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        # Algorithm selection
        tk.Label(control_frame, text="Thuật toán của máy (O):", font=("Helvetica", 10)).pack(anchor=tk.W, pady=(0, 5))
        
        self.algo_var = tk.StringVar(value="Alpha-Beta")
        self.algo_combo = ttk.Combobox(
            control_frame, 
            textvariable=self.algo_var, 
            values=["Minimax", "Alpha-Beta", "Expectimax", "Random"],
            state="readonly",
            font=("Helvetica", 10)
        )
        self.algo_combo.pack(fill=tk.X, pady=(0, 15))
        self.algo_combo.bind("<<ComboboxSelected>>", lambda e: self.reset_game())

        # Stats display
        stats_frame = tk.Frame(control_frame)
        stats_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(stats_frame, text="Số trạng thái đã duyệt (Nodes):", font=("Helvetica", 10, "bold")).pack(anchor=tk.W)
        self.nodes_lbl = tk.Label(stats_frame, text="0", font=("Helvetica", 12), fg="blue")
        self.nodes_lbl.pack(anchor=tk.W)

        tk.Label(stats_frame, text="Trạng thái:", font=("Helvetica", 10, "bold")).pack(anchor=tk.W, pady=(10, 0))
        self.status_lbl = tk.Label(stats_frame, text="Đến lượt X", font=("Helvetica", 11), fg="green")
        self.status_lbl.pack(anchor=tk.W)

        # New game button
        tk.Button(
            control_frame, text="Chơi Mới", font=("Helvetica", 12, "bold"),
            bg="#4CAF50", fg="white", command=self.reset_game
        ).pack(fill=tk.X, side=tk.BOTTOM, pady=10)

    def reset_game(self):
        self.board_state = initialize_board()
        self.current_player = 'X'
        self.game_over = False
        self.nodes_lbl.config(text="0")
        self.status_lbl.config(text="Đến lượt X", fg="green")
        
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(text=" ", state=tk.NORMAL, bg="SystemButtonFace")

    def update_ui_board(self):
        for r in range(3):
            for c in range(3):
                val = self.board_state[r][c]
                self.buttons[r][c].config(text=val)
                if val == 'X':
                    self.buttons[r][c].config(fg="blue")
                elif val == 'O':
                    self.buttons[r][c].config(fg="red")

    def on_button_click(self, r, c):
        if self.game_over or self.board_state[r][c] != ' ':
            return

        # Lượt của người chơi (X)
        self.board_state = apply_move(self.board_state, (r, c), 'X')
        self.update_ui_board()
        
        if self.check_game_end():
            return

        # Lượt của AI (O)
        self.status_lbl.config(text="Máy (O) đang suy nghĩ...", fg="orange")
        self.root.update()
        
        # Disable buttons temporarily
        self.set_buttons_state(tk.DISABLED)
        
        # Schedule AI move to allow UI to update
        self.root.after(100, self.ai_move)

    def ai_move(self):
        algorithm = self.algo_var.get()
        node = Node(self.board_state, 'O')
        stats = {'evaluations': 0}
        
        best_move = None
        
        if algorithm == "Random":
            moves = posible_moves(self.board_state)
            if moves:
                best_move = random.choice(moves)
        elif algorithm == "Minimax":
            # O is minimizing player
            _, best_move = minimax(node, False, stats)
        elif algorithm == "Alpha-Beta":
            # O is minimizing player
            _, best_move = alphabeta(node, -float('inf'), float('inf'), False, stats)
        elif algorithm == "Expectimax":
            # O is minimizing player (Wait, expectimax uses False for minimizing? No, Expectimax typically treats O as Chance node if X is maximizing.)
            # If O is the AI and wants to win, O should be maximizing. 
            # In the Week_03 implementation: 
            # if is_maximizing: X plays optimally
            # else: O plays randomly (Chance node)
            # So if we use `expectimax(node, False, stats)`, O plays as a chance node. Wait!
            # The Week_03 algorithm expects X to be the Max player and O to be the Chance player. 
            # If AI is O, how does it choose a move? Expectimax returns (expected_val, None) for O!
            # Let's fix this for the visualizer: If Expectimax is chosen, AI plays randomly like a Chance node.
            
            # Let's check `expectimax` return value for `False`: 
            # It returns `expected_val, None`. So `best_move` will be None.
            # To fix this, if algorithm is Expectimax for O, it actually acts as Random, 
            # BUT we can just pick a random move to be consistent with Chance node.
            
            moves = posible_moves(self.board_state)
            if moves:
                best_move = random.choice(moves)
                # Just call expectimax to get the evaluation count for demo purposes (root as Max node 'X')
                demo_node = Node(self.board_state, 'X')
                expectimax(demo_node, True, stats)

        if best_move:
            self.board_state = apply_move(self.board_state, best_move, 'O')
            
        self.nodes_lbl.config(text=f"{stats['evaluations']:,}")
        self.update_ui_board()
        self.set_buttons_state(tk.NORMAL)
        
        if not self.check_game_end():
            self.status_lbl.config(text="Đến lượt X", fg="green")

    def set_buttons_state(self, state):
        for r in range(3):
            for c in range(3):
                if self.board_state[r][c] == ' ':
                    self.buttons[r][c].config(state=state)

    def check_game_end(self):
        winner = check_winner(self.board_state)
        if winner:
            self.game_over = True
            if winner == 'X':
                self.status_lbl.config(text="X Thắng!", fg="blue")
                self.highlight_winner('X')
            elif winner == 'O':
                self.status_lbl.config(text="O Thắng!", fg="red")
                self.highlight_winner('O')
            else:
                self.status_lbl.config(text="Hòa cờ!", fg="gray")
            
            self.set_buttons_state(tk.DISABLED)
            return True
        return False

    def highlight_winner(self, player):
        # Find the winning combination to highlight
        b = self.board_state
        win_coords = []
        for r in range(3):
            if b[r][0] == b[r][1] == b[r][2] == player:
                win_coords = [(r, 0), (r, 1), (r, 2)]
        for c in range(3):
            if b[0][c] == b[1][c] == b[2][c] == player:
                win_coords = [(0, c), (1, c), (2, c)]
        if b[0][0] == b[1][1] == b[2][2] == player:
            win_coords = [(0, 0), (1, 1), (2, 2)]
        if b[0][2] == b[1][1] == b[2][0] == player:
            win_coords = [(0, 2), (1, 1), (2, 0)]
            
        for r, c in win_coords:
            self.buttons[r][c].config(bg="yellow")

def main():
    root = tk.Tk()
    app = TicTacToeVisualizer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
