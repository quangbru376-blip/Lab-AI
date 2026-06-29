import copy
import random

# =============================================================================
# Cấu trúc Node lưu trữ trạng thái Game (giống như bài Vacuum Cleaner)
# =============================================================================
class Node:
    def __init__(self, board_state, player, parent=None, birth_action=None, level=0):
        self.board_state = board_state  # Trạng thái bảng cờ (ma trận 3x3)
        self.player = player            # Người chơi chuẩn bị đi tiếp ('X' hoặc 'O')
        self.parent = parent            # Node cha
        self.birth_action = birth_action # Nước đi dẫn đến trạng thái này (dòng, cột)
        self.level = level              # Độ sâu của node (dùng để tối ưu hóa thời gian thắng)

# =============================================================================
# Khởi tạo và các hàm bổ trợ cho trò chơi Tic-Tac-Toe
# =============================================================================
ROW = 3
COL = 3

def initialize_board():
    """Khởi tạo bảng cờ 3x3 trống"""
    return [[' ' for _ in range(COL)] for _ in range(ROW)]

def posible_moves(board):
    """Tìm tất cả các nước đi hợp lệ (các ô còn trống)"""
    moves = []
    for r in range(ROW):
        for c in range(COL):
            if board[r][c] == ' ':
                moves.append((r, c))
    return moves

def apply_move(board, move, player):
    """Thực hiện nước đi và trả về trạng thái bảng mới"""
    temp_board = copy.deepcopy(board)
    temp_board[move[0]][move[1]] = player
    return temp_board

def check_winner(board):
    """
    Kiểm tra trạng thái kết thúc của bảng cờ:
    - Trả về 'X' nếu X thắng
    - Trả về 'O' nếu O thắng
    - Trả về 'Draw' nếu hòa cờ (hết ô trống)
    - Trả về None nếu game chưa kết thúc
    """
    # Kiểm tra các hàng ngang
    for r in range(ROW):
        if board[r][0] == board[r][1] == board[r][2] != ' ':
            return board[r][0]
            
    # Kiểm tra các cột dọc
    for c in range(COL):
        if board[0][c] == board[1][c] == board[2][c] != ' ':
            return board[0][c]
            
    # Kiểm tra đường chéo chính và đường chéo phụ
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]
        
    # Kiểm tra xem có còn ô trống nào không
    for r in range(ROW):
        for c in range(COL):
            if board[r][c] == ' ':
                return None  # Game vẫn tiếp tục
                
    return 'Draw'  # Hòa cờ

# =============================================================================
# Thuật toán 1: MINIMAX (Thuần túy, không cắt tỉa)
# =============================================================================
def minimax(node: Node, is_maximizing: bool, stats: dict):
    """
    Thuật toán Minimax truyền thống.
    - X đóng vai trò là Maximizing Player (tìm cách tăng điểm tối đa)
    - O đóng vai trò là Minimizing Player (tìm cách giảm điểm tối thiểu)
    """
    stats['evaluations'] += 1  # Tăng số node đã đánh giá
    
    winner = check_winner(node.board_state)
    
    # Điều kiện dừng (Trạng thái lá)
    if winner == 'X':
        return 10 - node.level, None  # Trừ node.level để ưu tiên thắng nhanh nhất
    if winner == 'O':
        return -10 + node.level, None  # Cộng node.level để ưu tiên trì hoãn thua lâu nhất
    if winner == 'Draw':
        return 0, None
        
    moves = posible_moves(node.board_state)
    
    if is_maximizing:
        max_val = -float('inf')
        best_move = None
        
        for move in moves:
            # Tạo node con từ nước đi thử nghiệm
            temp_board = apply_move(node.board_state, move, 'X')
            child_node = Node(temp_board, 'O', parent=node, birth_action=move, level=node.level + 1)
            
            # Đệ quy tìm giá trị Minimax của node con
            val, _ = minimax(child_node, False, stats)
            
            if val > max_val:
                max_val = val
                best_move = move
                
        return max_val, best_move
    else:
        min_val = float('inf')
        best_move = None
        
        for move in moves:
            # Tạo node con từ nước đi thử nghiệm
            temp_board = apply_move(node.board_state, move, 'O')
            child_node = Node(temp_board, 'X', parent=node, birth_action=move, level=node.level + 1)
            
            # Đệ quy tìm giá trị Minimax của node con
            val, _ = minimax(child_node, True, stats)
            
            if val < min_val:
                min_val = val
                best_move = move
                
        return min_val, best_move

# =============================================================================
# Thuật toán 2: ALPHA-BETA MINIMAX (Cắt tỉa Alpha-Beta)
# =============================================================================
def alphabeta(node: Node, alpha: float, beta: float, is_maximizing: bool, stats: dict):
    """
    Thuật toán Minimax kết hợp cắt tỉa Alpha-Beta để giảm số lượng node cần duyệt.
    - alpha: Giá trị tốt nhất mà Maximizing Player (X) chắc chắn đạt được.
    - beta: Giá trị tốt nhất mà Minimizing Player (O) chắc chắn đạt được.
    """
    stats['evaluations'] += 1  # Tăng số node đã đánh giá
    
    winner = check_winner(node.board_state)
    
    # Điều kiện dừng (Trạng thái lá)
    if winner == 'X':
        return 10 - node.level, None
    if winner == 'O':
        return -10 + node.level, None
    if winner == 'Draw':
        return 0, None
        
    moves = posible_moves(node.board_state)
    
    if is_maximizing:
        max_val = -float('inf')
        best_move = None
        
        for move in moves:
            temp_board = apply_move(node.board_state, move, 'X')
            child_node = Node(temp_board, 'O', parent=node, birth_action=move, level=node.level + 1)
            
            val, _ = alphabeta(child_node, alpha, beta, False, stats)
            
            if val > max_val:
                max_val = val
                best_move = move
                
            alpha = max(alpha, val)
            if beta <= alpha:
                break  # Cắt tỉa Beta (O sẽ không bao giờ chọn nhánh này)
                
        return max_val, best_move
    else:
        min_val = float('inf')
        best_move = None
        
        for move in moves:
            temp_board = apply_move(node.board_state, move, 'O')
            child_node = Node(temp_board, 'X', parent=node, birth_action=move, level=node.level + 1)
            
            val, _ = alphabeta(child_node, alpha, beta, True, stats)
            
            if val < min_val:
                min_val = val
                best_move = move
                
            beta = min(beta, val)
            if beta <= alpha:
                break  # Cắt tỉa Alpha (X sẽ không bao giờ chọn nhánh này)
                
        return min_val, best_move

# =============================================================================
# Thuật toán 3: EXPECTIMAX (Tính toán giá trị kỳ vọng)
# =============================================================================
def expectimax(node: Node, is_maximizing: bool, stats: dict):
    """
    Thuật toán Expectimax.
    - Max Node (X): Người chơi tính toán để tối đa hóa điểm số của mình.
    - Chance Node (O): Đại diện cho yếu tố ngẫu nhiên (đối thủ chơi ngẫu nhiên không tối ưu).
      Tại đây ta tính giá trị kỳ vọng (trung bình cộng điểm số của các nước đi hợp lệ).
    """
    stats['evaluations'] += 1  # Tăng số node đã đánh giá
    
    winner = check_winner(node.board_state)
    
    # Điều kiện dừng (Trạng thái lá)
    if winner == 'X':
        return 10 - node.level, None
    if winner == 'O':
        return -10 + node.level, None
    if winner == 'Draw':
        return 0, None
        
    moves = posible_moves(node.board_state)
    
    if is_maximizing:
        max_val = -float('inf')
        best_move = None
        
        for move in moves:
            temp_board = apply_move(node.board_state, move, 'X')
            child_node = Node(temp_board, 'O', parent=node, birth_action=move, level=node.level + 1)
            
            val, _ = expectimax(child_node, False, stats)
            
            if val > max_val:
                max_val = val
                best_move = move
                
        return max_val, best_move
    else:
        # Chance Node: Tính trung bình cộng của tất cả các nhánh có thể đi của O
        total_val = 0
        
        for move in moves:
            temp_board = apply_move(node.board_state, move, 'O')
            child_node = Node(temp_board, 'X', parent=node, birth_action=move, level=node.level + 1)
            
            val, _ = expectimax(child_node, True, stats)
            total_val += val
            
        # Xác suất mỗi ô trống được đánh là như nhau = 1 / len(moves)
        expected_val = total_val / len(moves)
        return expected_val, None

# =============================================================================
# In đường đi (giống như cách in đường đi path(goal_node) của robot hút bụi)
# =============================================================================
def print_game_path(goal_node: Node):
    """Truy vết ngược từ Node đích về Node gốc để in toàn bộ tiến trình trận đấu"""
    current = goal_node
    game_path = []
    
    while current.parent is not None:
        game_path.append(current)
        current = current.parent
    game_path.append(current)
    game_path.reverse()
    
    for i, node in enumerate(game_path):
        if i == 0:
            print("Trạng thái bắt đầu (Initial board):")
        else:
            print(f"Bước đi thứ: {i}")
            print(f"Người chơi vừa đi: {node.parent.player}")
            print(f"Vị trí đánh: Dòng {node.birth_action[0]}, Cột {node.birth_action[1]}")
        
        # Vẽ bảng cờ
        for row in node.board_state:
            print(f" {row} ")
        print("=" * 25)

# =============================================================================
# Hàm Main chạy thực tế và so sánh hiệu năng
# =============================================================================
def main():
    print("=== MÔ PHỎNG THUẬT TOÁN ĐỐI KHÁNG TI-TAC-TOE ===")
    
    # 1. Chạy mô phỏng trận đấu hoàn chỉnh (X dùng Expectimax, O chơi ngẫu nhiên)
    board = initialize_board()
    root = Node(board, 'X')
    current_node = root
    
    print("\n--- Đang giả lập trận đấu (X: Expectimax, O: Random) ---")
    while check_winner(current_node.board_state) is None:
        if current_node.player == 'X':
            # X đi bằng Expectimax
            stats = {'evaluations': 0}
            _, best_move = expectimax(current_node, True, stats)
            new_board = apply_move(current_node.board_state, best_move, 'X')
            current_node = Node(new_board, 'O', parent=current_node, birth_action=best_move, level=current_node.level + 1)
        else:
            # O đi ngẫu nhiên
            moves = posible_moves(current_node.board_state)
            random_move = random.choice(moves)
            new_board = apply_move(current_node.board_state, random_move, 'O')
            current_node = Node(new_board, 'X', parent=current_node, birth_action=random_move, level=current_node.level + 1)
            
    # In ra toàn bộ diễn biến trận đấu
    print_game_path(current_node)
    
    winner = check_winner(current_node.board_state)
    if winner == 'Draw':
        print(">>> Kết quả: Hòa cờ!")
    else:
        print(f">>> Kết quả: Người chơi {winner} Thắng cuộc!")
        
    # 2. So sánh hiệu năng giữa Minimax, Alpha-Beta và Expectimax
    print("\n" + "="*50)
    print("SO SÁNH SỐ NODE CẦN DUYỆT (Bảng cờ ban đầu rỗng):")
    print("="*50)
    
    # Khởi tạo trạng thái rỗng để tính toán nước đi đầu tiên cho X
    test_board = initialize_board()
    test_root = Node(test_board, 'X')
    
    # Đo hiệu năng Minimax thuần túy
    minimax_stats = {'evaluations': 0}
    _, m_move = minimax(test_root, True, minimax_stats)
    print(f"[-] Thuật toán Minimax thuần túy:")
    print(f"    + Nước đi tốt nhất đề xuất: {m_move}")
    print(f"    + Số lượng trạng thái đã đánh giá: {minimax_stats['evaluations']:,} node")
    
    # Đo hiệu năng Alpha-Beta Pruning
    ab_stats = {'evaluations': 0}
    _, ab_move = alphabeta(test_root, -float('inf'), float('inf'), True, ab_stats)
    print(f"[-] Thuật toán Alpha-Beta Minimax:")
    print(f"    + Nước đi tốt nhất đề xuất: {ab_move}")
    print(f"    + Số lượng trạng thái đã đánh giá: {ab_stats['evaluations']:,} node")
    
    # Đo hiệu năng Expectimax
    exp_stats = {'evaluations': 0}
    _, exp_move = expectimax(test_root, True, exp_stats)
    print(f"[-] Thuật toán Expectimax:")
    print(f"    + Nước đi tốt nhất đề xuất: {exp_move}")
    print(f"    + Số lượng trạng thái đã đánh giá: {exp_stats['evaluations']:,} node")
    
    print("="*50)
    saved_nodes = minimax_stats['evaluations'] - ab_stats['evaluations']
    percent_saved = (saved_nodes / minimax_stats['evaluations']) * 100
    print(f"--> Alpha-Beta Pruning đã tiết kiệm được: {saved_nodes:,} node ({percent_saved:.2f}%) so với Minimax thuần túy!")
    print("--> Expectimax không thể cắt tỉa (do tính trung bình cộng), nên số node duyệt lớn bằng Minimax thuần túy.")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
