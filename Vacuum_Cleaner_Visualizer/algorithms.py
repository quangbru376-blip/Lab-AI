# Cả 4 thuật toán
import random
import copy
import math

class Node:
    def __init__(self, floor_state, position: tuple, parent, birth_action):
        self.floor_state = floor_state
        self.position = position
        self.parent = parent
        self.birth_action = birth_action
        self.depth = 0
        self.level = 0
        self.cost = 0
        # dùng cho A Star
        self.path_cost = 0
        self.heuristic_cost = 0
        self.total = 0
    
    def cal_total_cost(self):
        self.total_cost = self.path_cost + self.heuristic_cost
        
    def get_tuple_floor_state(self):
        return tuple(tuple(row) for row in self.floor_state)

class Queue:
    def __init__(self):
        self.queue = []
        
    def is_empty(self):
        return len(self.queue) == 0
    
    def enqueue(self, node):
        self.queue.append(node)
        
    def dequeue(self) -> Node:
        return self.queue.pop(0)
    
    def pop(self, index: int):
        return self.queue.pop(index)
        
    def pop_the_highest_priority(self) -> Node:
        #thêm 1 phương thức pop ưu tiên cao nhất (cost thấp nhất) trong queue
        max_priority_index = 0
        for i in range(len(self.queue)):
            if self.queue[i].cost < self.queue[max_priority_index].cost:
                max_priority_index = i
        return self.queue.pop(max_priority_index)
    
    def contain(self, other: Node):
        for i, node in enumerate(self.queue):
            if node.floor_state == other.floor_state and node.position == other.position:
                return i
        return -1

class Stack:
    def __init__(self):
        self.stack = []

    def is_empty(self):
        return len(self.stack) == 0

    def push(self, node: Node):
        self.stack.append(node)

    def pop(self) -> Node:
        return self.stack.pop()

    def contain(self, other: Node):
        for node in self.stack:
            if node.floor_state == other.floor_state and node.position == other.position:
                return True
        return False

ROW, COL = 5, 5
GOAL_STATE = [[0 for _ in range(COL)] for _ in range(ROW)]

def floor_and_vacuumpos_initialize():
    floor = [[0 for _ in range(COL)] for _ in range(ROW)]
    vacuum_pos = (random.randint(0, ROW - 1), random.randint(0, COL - 1))
    
    # Sinh ngẫu nhiên từ 3 đến 6 ô dơ (rác)
    num_dirty = random.randint(3, 6)
    dirty_tiles = set()
    while len(dirty_tiles) < num_dirty:
        r = random.randint(0, ROW - 1)
        c = random.randint(0, COL - 1)
        if (r, c) != vacuum_pos:
            dirty_tiles.add((r, c))
            
    for r, c in dirty_tiles:
        floor[r][c] = 1
        
    return floor, vacuum_pos


def static_initialize():
    # Khởi tạo bản đồ 5x5 cố định đối xứng
    floor = [
        [0, 1, 0, 0, 0],
        [1, 0, 0, 1, 0],
        [0, 0, 0, 0, 0],
        [1, 0, 0, 0, 1],
        [0, 0, 0, 1, 0]
    ]
    vacuum_pos = (2, 2)
    return floor, vacuum_pos



def posible_moves(vacuum_pos):
    moves = []
    if vacuum_pos[0] > 0: moves.append("UP")
    if vacuum_pos[0] < ROW - 1: moves.append("DOWN")
    if vacuum_pos[1] > 0: moves.append("LEFT")
    if vacuum_pos[1] < COL - 1: moves.append("RIGHT")
    return moves

def apply_move(floor, vacuum_pos, move):
    temp_floor = copy.deepcopy(floor)
    if move == "UP": temp_vac_pos = (vacuum_pos[0] - 1, vacuum_pos[1])
    elif move == "DOWN": temp_vac_pos = (vacuum_pos[0] + 1, vacuum_pos[1])
    elif move == "LEFT": temp_vac_pos = (vacuum_pos[0], vacuum_pos[1] - 1)
    else: temp_vac_pos = (vacuum_pos[0], vacuum_pos[1] + 1)
    
    if temp_floor[temp_vac_pos[0]][temp_vac_pos[1]] == 1:
        temp_floor[temp_vac_pos[0]][temp_vac_pos[1]] = 0 
    return temp_floor, temp_vac_pos

def get_n0_of_dirty_tiles(floor: list) -> int:
    """
    Counting the number of dirty tiles
    """
    number_of_dirty_tile = 0
    for row in floor:
        for tile in row:
            if tile == 1:
                number_of_dirty_tile += 1
    return number_of_dirty_tile

def find_dirty_tiles_position(floor) -> list:
    """
    Find all the position (x, y) of dirty tiles on the floor

    """
    positions = []
    for row in range(ROW):
        for col in range(COL):
            if floor[row][col] == 1:
                positions.append((row, col))
    return positions

def min_manhattan_distance(floor, vacuum_pos) -> int:
    """
    Find the nearest dirty tiles
    """
    dirty_tiles = find_dirty_tiles_position(floor)
    if not dirty_tiles:
        return 0
    dis = abs(dirty_tiles[0][0]-vacuum_pos[0]) + abs(dirty_tiles[0][1]-vacuum_pos[1])
    for pos in dirty_tiles:
        temp_dis = abs(pos[0]-vacuum_pos[0]) + abs(pos[1]-vacuum_pos[1])
        if dis > temp_dis:
            dis = temp_dis
    return dis

def generate_path_list(goal_node, goal_reached):
    """Hàm bổ trợ trích xuất đường đi từ goal_node về root thành một list các tuple (node, is_final_step)"""
    if goal_node is not None:
        actual_path = []
        current = goal_node
        while current.parent is not None:
            actual_path.append(current)
            current = current.parent
        actual_path.append(current)
        actual_path.reverse()
        
        path_list = []
        if goal_reached:
            for index, node in enumerate(actual_path):
                is_final_step = (index == len(actual_path) - 1)
                path_list.append((node, is_final_step))
        else:
            for node in actual_path:
                path_list.append((node, False))
            path_list.append((None, False))
        return path_list
    else:
        return [(None, False)]



def get_heuristic_cost(floor, vacuum_pos) -> int:
    dirty_count = get_n0_of_dirty_tiles(floor)
    return dirty_count


def has_cycle(node: Node) -> bool:
    curr = node.parent
    while curr is not None:
        if curr.floor_state == node.floor_state and curr.position == node.position:
            return True
        curr = curr.parent
    return False


def search_ida(root: Node, bound: int) -> tuple:
    root.cal_total_cost()
    if root.total_cost > bound:
        return "LIMIT", root.total_cost
    if root.floor_state == GOAL_STATE:
        return "FOUND", root
        
    stack = Stack()
    stack.push(root)
    
    min_exceeded = float('inf')
    visited = {}  # key: (floor_tuple, position) -> min_path_cost
    
    while not stack.is_empty():
        curr_node = stack.pop()
        
        state_key = (curr_node.get_tuple_floor_state(), curr_node.position)
        if state_key in visited and visited[state_key] <= curr_node.path_cost:
            continue
        visited[state_key] = curr_node.path_cost
        
        if curr_node.floor_state == GOAL_STATE:
            return "FOUND", curr_node
            
        moves = posible_moves(curr_node.position)
        for move in moves:
            temp_floor, temp_vacuum_pos = apply_move(curr_node.floor_state, curr_node.position, move)
            child = Node(temp_floor, temp_vacuum_pos, parent=curr_node, birth_action=move)
            
            if has_cycle(child):
                continue
                
            child.path_cost = get_n0_of_dirty_tiles(temp_floor) + curr_node.path_cost
            child.heuristic_cost = min_manhattan_distance(temp_floor, temp_vacuum_pos)
            child.cal_total_cost()
            
            f = child.total_cost
            
            if f > bound:
                if f < min_exceeded:
                    min_exceeded = f
                continue
                
            child_state_key = (child.get_tuple_floor_state(), child.position)
            if child_state_key not in visited or visited[child_state_key] > child.path_cost:
                stack.push(child)
            
    return "LIMIT", min_exceeded


#
#=============================================================================
#A Star - ưu tiên node có cost f(n) = g(n) + h(n) (số ô bẩn + khoảng cách Manhattan)
#
def run_A_Star(floor, vacuum_pos):
    """
    Chi phí sử dụng trong bài:
        - h(n): Khoảng cách Manhattan
        - g(n): số ô dơ
    """
    frontier = Queue()
    root = Node(floor_state=floor, position=vacuum_pos, parent=None, birth_action= None)
    root.path_cost = get_n0_of_dirty_tiles(floor)
    root.heuristic_cost = min_manhattan_distance(floor, vacuum_pos)
    root.cal_total_cost()
    frontier.enqueue(root)
    visited_state = set()
    goal_node = None
    step = 0
    
    while True:
        if frontier.is_empty(): #dừng khi frontier trống (hết cách)
            print("Frontier is empty!!")
            break
        
        current_node = frontier.pop_the_highest_priority()
        step += 1
        if (current_node.get_tuple_floor_state(), current_node.position) not in visited_state: #check nếu state node có trong visited
            visited_state.add((current_node.get_tuple_floor_state(), current_node.position))
        else:
            continue
        
        if current_node.floor_state == GOAL_STATE: #dừng khi tìm thấy đáp án (GOAL)
            goal_node = current_node
            break
        
        moves = posible_moves(current_node.position)
        for move in moves:
            # chạy thử từng bước có thể để sinh node con
            temp_floor, temp_vacuum_pos = apply_move(current_node.floor_state, current_node.position, move)
            temp_node = Node(temp_floor, temp_vacuum_pos, current_node, move) #sinh node con
            temp_node.path_cost = get_n0_of_dirty_tiles(temp_floor) + current_node.path_cost
            temp_node.heuristic_cost = min_manhattan_distance(temp_floor, temp_vacuum_pos)
            temp_node.cal_total_cost()
                        
            if frontier.contain(temp_node)== -1 and (temp_node.get_tuple_floor_state(), temp_vacuum_pos) not in visited_state:
                #kiểm tra nếu node con không có trong visited hoặc frontier
                frontier.enqueue(temp_node)
                
                #nếu có 1 node có cùng state nhưng total cost tốt hơn thì thay thế node đó
            elif frontier.contain(temp_node) != -1:
                target_index = frontier.contain(temp_node)
                target_node = frontier.queue[target_index]
                if temp_node.total_cost < target_node.total_cost:
                    frontier.pop(target_index)
                    frontier.enqueue(temp_node)
                    
    return generate_path_list(goal_node, True)
#
#=============================================================================
#GREEDY - ưu tiên node có cost (ô bẩn) thấp nhất so với GOAL
#
def run_greedy(floor, vacuum_pos):
    frontier = Queue()
    root = Node(floor_state=floor, position=vacuum_pos, parent=None, birth_action= None)
    root.cost= get_n0_of_dirty_tiles(floor)
    frontier.enqueue(root)
    visited_state = set()
    step = 0
    goal_node = None
    
    while True:
        if frontier.is_empty(): #dừng khi frontier trống (hết cách)
            print("Frontier is empty!!")
            break
        
        current_node = frontier.pop_the_highest_priority()
        step += 1
        if (current_node.get_tuple_floor_state(), current_node.position) not in visited_state: #check nếu state node có trong visited
            visited_state.add((current_node.get_tuple_floor_state(), current_node.position))
        else:
            continue
        
        if current_node.floor_state == GOAL_STATE: #dừng khi tìm thấy đáp án (GOAL)
            goal_node = current_node
            break
        
        moves = posible_moves(current_node.position)
        for move in moves:
            # chạy thử từng bước có thể để sinh node con
            temp_floor, temp_vacuum_pos = apply_move(current_node.floor_state, current_node.position, move)
            temp_node = Node(temp_floor, temp_vacuum_pos, current_node, move) #sinh node con
            temp_node.cost = get_n0_of_dirty_tiles(temp_floor)
            
            if frontier.contain(temp_node)== -1 and (temp_node.get_tuple_floor_state(), temp_vacuum_pos) not in visited_state:
                #kiểm tra nếu node con không có trong visited hoặc frontier
                frontier.enqueue(temp_node)
    
    return generate_path_list(goal_node, True)
#
#=============================================================================
#UCS Priority Queue - ưu tiên node có cost (ô bẩn) thấp nhất
#
def run_uniform_cost_search(floor, vacuum_pos):
    frontier = Queue()
    root = Node(floor_state=floor, position=vacuum_pos, parent=None, birth_action= None)
    root.cost = get_n0_of_dirty_tiles(floor)
    frontier.enqueue(root)
    visited_state = set()
    step = 0
    
    while True:
        if frontier.is_empty(): #dừng khi frontier trống (hết cách)
            print("Frontier is empty!!")
            break
        
        current_node = frontier.pop_the_highest_priority()
        step += 1
        if (current_node.get_tuple_floor_state(), current_node.position) not in visited_state: #check nếu state node có trong visited
            visited_state.add((current_node.get_tuple_floor_state(), current_node.position))
        else:
            continue
        
        if current_node.floor_state == GOAL_STATE: #dừng khi tìm thấy đáp án (GOAL)
            goal_node = current_node
            break
        
        moves = posible_moves(current_node.position)
        for move in moves:# chạy thử từng bước có thể để sinh node con
            temp_floor, temp_vacuum_pos = apply_move(current_node.floor_state, current_node.position, move)
            temp_node_cost = get_n0_of_dirty_tiles(temp_floor)
            temp_node = Node(temp_floor, temp_vacuum_pos, current_node, move) #sinh node con
            temp_node.cost = current_node.cost + temp_node_cost
            
            if frontier.contain(temp_node)== -1 and (temp_node.get_tuple_floor_state(), temp_vacuum_pos) not in visited_state:
                #kiểm tra nếu node con không có trong visited hoặc frontier
                frontier.enqueue(temp_node)
                
                #nếu có 1 node có cùng state nhưng cost tốt hơn thì thay thế node đó
            elif frontier.contain(temp_node) != -1:
                target_index = frontier.contain(temp_node)
                target_node = frontier.queue[target_index]
                if temp_node.cost < target_node.cost:
                    frontier.pop(target_index)
                    frontier.enqueue(temp_node)
                
    return generate_path_list(goal_node, True)
#=============================================================================
#IDS - Kiểm tra Goal State khi sinh con
def early_depth_limit_search(start_floor: list, vacuum_pos: tuple, depth):
    frontier = Stack()
    root = Node(floor_state=start_floor, position=vacuum_pos, birth_action=None, parent=None)
    frontier.push(root)
    visited_state = {}  # key: (floor_tuple, position) -> min_depth
    result = "FAILURE"
    while not frontier.is_empty():
        current_node = frontier.pop()
        
        #kiểm tra và trả về node nếu tìm thấy
        if current_node.floor_state == GOAL_STATE:
            return current_node

        #kiểm tra xem state của node đang xét có trong visited hay không
        state_key = (current_node.get_tuple_floor_state(), current_node.position)
        if state_key in visited_state and visited_state[state_key] <= current_node.depth:
            continue
        visited_state[state_key] = current_node.depth
            
        if current_node.depth >= depth:
            result = "CUTOFF"
        else:
            moves = posible_moves(current_node.position)
            for move in moves:
                temp_floor, temp_position = apply_move(current_node.floor_state, current_node.position, move)
                temp_node = Node(floor_state=temp_floor, position=temp_position, parent=current_node, birth_action= move)
                temp_node.depth = current_node.depth + 1
                #kiểm tra goal khi sinh con (Early Goal Check)
                if temp_node.floor_state == GOAL_STATE:
                    return temp_node
                if not frontier.contain(temp_node):
                    child_state_key = (temp_node.get_tuple_floor_state(), temp_node.position)
                    if child_state_key not in visited_state or visited_state[child_state_key] > temp_node.depth:
                        frontier.push(temp_node)
                
    
    return result

def run_early_iterative_deepening_search(floor: list, vacuum_pos: tuple):
    depth = 0
    
    while True:
        result = early_depth_limit_search(start_floor=floor, vacuum_pos=vacuum_pos, depth= depth)
        if result != "CUTOFF":
            break
        depth += 1
    
    if result == "FAILURE":
        result = None
    return generate_path_list(result, result is not None)
#=============================================================================
#IDS - Chỉ kiểm tra Goal State khi lấy ra từ queue
def late_depth_limit_search(start_floor: list, vacuum_pos: tuple, depth):
    frontier = Stack()
    root = Node(floor_state=start_floor, position=vacuum_pos, birth_action=None, parent=None)
    frontier.push(root)
    visited_state = {}  # key: (floor_tuple, position) -> min_depth
    result = "FAILURE"
    while not frontier.is_empty():
        current_node = frontier.pop()
        
        #kiểm tra và trả về node nếu tìm thấy
        if current_node.floor_state == GOAL_STATE:
            return current_node

        #kiểm tra xem state của node đang xét có trong visited hay không
        state_key = (current_node.get_tuple_floor_state(), current_node.position)
        if state_key in visited_state and visited_state[state_key] <= current_node.depth:
            continue
        visited_state[state_key] = current_node.depth
            
        if current_node.depth >= depth:
            result = "CUTOFF"
        else:
            moves = posible_moves(current_node.position)
            for move in moves:
                temp_floor, temp_position = apply_move(current_node.floor_state, current_node.position, move)
                temp_node = Node(floor_state=temp_floor, position=temp_position, parent=current_node, birth_action= move)
                temp_node.depth = current_node.depth + 1
                if not frontier.contain(temp_node):
                    child_state_key = (temp_node.get_tuple_floor_state(), temp_node.position)
                    if child_state_key not in visited_state or visited_state[child_state_key] > temp_node.depth:
                        frontier.push(temp_node)
    
    return result

def run_late_iterative_deepening_search(floor: list, vacuum_pos: tuple):
    depth = 0
    
    while True:
        result = late_depth_limit_search(start_floor=floor, vacuum_pos=vacuum_pos, depth= depth)
        if result != "CUTOFF":
            break
        depth += 1
    
    if result == "FAILURE":
        result = None
    return generate_path_list(result, result is not None)

#
#=============================================================================
#BFS - Kiểm tra Goal State khi sinh con
def run_bfs_early(initial_floor, initial_vacuum_pos):
    frontier = Queue()
    visited_state = []
    root = Node(initial_floor, initial_vacuum_pos, None, None)
    frontier.enqueue(root)
    goal_node, goal_reached = None, False

    while not frontier.is_empty():
        current_node = frontier.dequeue()
        floor_tuple = tuple(tuple(row) for row in current_node.floor_state)
        if (floor_tuple, current_node.position) not in visited_state:
            visited_state.append((floor_tuple, current_node.position))
        else:
            continue

        moves = posible_moves(current_node.position)
        for move in moves:
            temp_floor, temp_vacuum_pos = apply_move(current_node.floor_state, current_node.position, move)
            temp_node = Node(temp_floor, temp_vacuum_pos, current_node, move)
            temp_node.level = current_node.level + 1
            
            if temp_floor == GOAL_STATE:
                goal_node, goal_reached = temp_node, True
                break
            
            temp_floor_tuple = tuple(tuple(row) for row in temp_floor)
            if frontier.contain(temp_node) == -1 and (temp_floor_tuple, temp_vacuum_pos) not in visited_state:
                frontier.enqueue(temp_node)
        if goal_reached: break

    return generate_path_list(goal_node, goal_reached)



#
#=============================================================================
#BFS - Chỉ kiểm tra Goal State khi lấy ra từ queue
def run_bfs_late(initial_floor, initial_vacuum_pos):
    frontier = Queue()
    visited_state = []
    root = Node(initial_floor, initial_vacuum_pos, None, None)
    frontier.enqueue(root)
    goal_node, goal_reached = None, False

    while not frontier.is_empty():
        current_node = frontier.dequeue()
        floor_tuple = tuple(tuple(row) for row in current_node.floor_state)
        if (floor_tuple, current_node.position) not in visited_state:
            visited_state.append((floor_tuple, current_node.position))
        else:
            continue

        if current_node.floor_state == GOAL_STATE:
            goal_node, goal_reached = current_node, True
            break

        moves = posible_moves(current_node.position)
        for move in moves:
            temp_floor, temp_vacuum_pos = apply_move(current_node.floor_state, current_node.position, move)
            temp_node = Node(temp_floor, temp_vacuum_pos, current_node, move)
            temp_node.level = current_node.level + 1
            
            temp_floor_tuple = tuple(tuple(row) for row in temp_floor)
            if frontier.contain(temp_node) == -1 and (temp_floor_tuple, temp_vacuum_pos) not in visited_state:
                frontier.enqueue(temp_node)
        if goal_reached: break

    return generate_path_list(goal_node, goal_reached)



#
#=============================================================================
#BFS - Kiểm tra Goal State khi sinh con
def run_dfs_early(initial_floor, initial_vacuum_pos):
    frontier = Stack()
    visited_state = []
    root = Node(initial_floor, initial_vacuum_pos, None, None)
    frontier.push(root)
    goal_node, goal_reached = None, False

    while not frontier.is_empty():
        current_node = frontier.pop()
        floor_tuple = tuple(tuple(row) for row in current_node.floor_state)
        if (floor_tuple, current_node.position) not in visited_state:
            visited_state.append((floor_tuple, current_node.position))
        else:
            continue

        moves = posible_moves(current_node.position)
        for move in moves:
            temp_floor, temp_vacuum_pos = apply_move(current_node.floor_state, current_node.position, move)
            temp_node = Node(temp_floor, temp_vacuum_pos, current_node, move)
            temp_node.level = current_node.level + 1
            
            if temp_floor == GOAL_STATE:
                goal_node, goal_reached = temp_node, True
                break
            
            temp_floor_tuple = tuple(tuple(row) for row in temp_floor)
            if not frontier.contain(temp_node) and (temp_floor_tuple, temp_vacuum_pos) not in visited_state:
                frontier.push(temp_node)
        if goal_reached: break

    return generate_path_list(goal_node, goal_reached)




#
#=============================================================================
#BFS - Chỉ kiểm tra Goal State khi lấy ra từ stack
def run_dfs_late(initial_floor, initial_vacuum_pos):
    frontier = Stack()
    visited_state = []
    root = Node(initial_floor, initial_vacuum_pos, None, None)
    frontier.push(root)
    goal_node, goal_reached = None, False

    while not frontier.is_empty():
        current_node = frontier.pop()
        floor_tuple = tuple(tuple(row) for row in current_node.floor_state)
        if (floor_tuple, current_node.position) not in visited_state:
            visited_state.append((floor_tuple, current_node.position))
        else:
            continue

        if current_node.floor_state == GOAL_STATE:
            goal_node, goal_reached = current_node, True
            break

        moves = posible_moves(current_node.position)
        for move in moves:
            temp_floor, temp_vacuum_pos = apply_move(current_node.floor_state, current_node.position, move)
            temp_node = Node(temp_floor, temp_vacuum_pos, current_node, move)
            temp_node.level = current_node.level + 1
            
            temp_floor_tuple = tuple(tuple(row) for row in temp_floor)
            if not frontier.contain(temp_node) and (temp_floor_tuple, temp_vacuum_pos) not in visited_state:
                frontier.push(temp_node)
        if goal_reached: break

    return generate_path_list(goal_node, goal_reached)


def run_ida_star(floor, vacuum_pos):
    root = Node(floor_state=floor, position=vacuum_pos, parent=None, birth_action=None)
    root.path_cost = get_n0_of_dirty_tiles(floor)
    root.heuristic_cost = min_manhattan_distance(floor, vacuum_pos)
    root.cal_total_cost()
    
    bound = root.total_cost
    goal_node = None
    
    iteration = 1
    max_iterations = 1000
    while iteration <= max_iterations:
        status, val = search_ida(root, bound)
        if status == "FOUND":
            goal_node = val
            break
        if val == float('inf'):
            break
        bound = val
        iteration += 1
        
    return generate_path_list(goal_node, goal_node is not None)

#
#=============================================================================
#Leo đồi đơn giản
#
def run_simple_hill_climbing(floor, vacuum_pos):
    current_node = Node(floor_state=floor, position=vacuum_pos, parent=None, birth_action=None)
    current_node.heuristic_cost = get_heuristic_cost(floor, vacuum_pos)
    
    if floor == GOAL_STATE:
        return generate_path_list(current_node, True)
        
    while True:
        can_continue = False
        moves = posible_moves(current_node.position)
        
        for move in moves:
            temp_floor, temp_vacuum_pos = apply_move(current_node.floor_state, current_node.position, move)
            child_heuristic_cost = get_heuristic_cost(temp_floor, temp_vacuum_pos)
            
            if child_heuristic_cost < current_node.heuristic_cost:
                child_node = Node(temp_floor, temp_vacuum_pos, current_node, move)
                child_node.heuristic_cost = child_heuristic_cost
                current_node = child_node
                can_continue = True
                break
        
        if current_node.floor_state == GOAL_STATE:
            return generate_path_list(current_node, True)
            
        if not can_continue:
            return generate_path_list(current_node, False)

#
#=============================================================================
#Leo đồi dốc nhất
#
def run_steepest_hill_climbing(floor, vacuum_pos):
    current_node = Node(floor_state=floor, position=vacuum_pos, parent=None, birth_action=None)
    current_node.heuristic_cost = get_heuristic_cost(floor, vacuum_pos)
    
    if floor == GOAL_STATE:
        return generate_path_list(current_node, True)

    while True:
        can_continue = False
        moves = posible_moves(current_node.position)
        children = []
        
        for move in moves:
            temp_floor, temp_vacuum_pos = apply_move(current_node.floor_state, current_node.position, move)
            child_heuristic_cost = get_heuristic_cost(temp_floor, temp_vacuum_pos)
            
            if child_heuristic_cost < current_node.heuristic_cost:
                child_node = Node(temp_floor, temp_vacuum_pos, current_node, move)
                child_node.heuristic_cost = child_heuristic_cost
                children.append(child_node)
                
        if children:
            current_node = min(children, key=lambda x: x.heuristic_cost)
            can_continue = True
            
        if current_node.floor_state == GOAL_STATE:
            return generate_path_list(current_node, True)
            
        if not can_continue:
            return generate_path_list(current_node, False)

#
#=============================================================================
#Leo đồi ngẫu nhiên
#
def run_stochastic_hill_climbing(floor, vacuum_pos):
    current_node = Node(floor_state=floor, position=vacuum_pos, parent=None, birth_action=None)
    current_node.heuristic_cost = get_heuristic_cost(floor, vacuum_pos)
    
    if floor == GOAL_STATE:
        return generate_path_list(current_node, True)

    while True:
        can_continue = False
        moves = posible_moves(current_node.position)
        children = []
        
        for move in moves:
            temp_floor, temp_vacuum_pos = apply_move(current_node.floor_state, current_node.position, move)
            child_heuristic_cost = get_heuristic_cost(temp_floor, temp_vacuum_pos)
            
            if child_heuristic_cost < current_node.heuristic_cost:
                child_node = Node(temp_floor, temp_vacuum_pos, current_node, move)
                child_node.heuristic_cost = child_heuristic_cost
                children.append(child_node)
                
        if children:
            current_node = random.choice(children)
            can_continue = True
            
        if current_node.floor_state == GOAL_STATE:
            return generate_path_list(current_node, True)
            
        if not can_continue:
            return generate_path_list(current_node, False)

#
#=============================================================================
#Leo đồi dốc nhất thêm điều kiện bằng
#
def run_equal_steepest_hill_climbing(floor, vacuum_pos):
    current_node = Node(floor_state=floor, position=vacuum_pos, parent=None, birth_action=None)
    current_node.heuristic_cost = get_heuristic_cost(floor, vacuum_pos)
    
    if floor == GOAL_STATE:
        return generate_path_list(current_node, True)

    while True:
        can_continue = False
        moves = posible_moves(current_node.position)
        children = []
        
        for move in moves:
            temp_floor, temp_vacuum_pos = apply_move(current_node.floor_state, current_node.position, move)
            child_heuristic_cost = get_heuristic_cost(temp_floor, temp_vacuum_pos)
            
            if child_heuristic_cost <= current_node.heuristic_cost:
                child_node = Node(temp_floor, temp_vacuum_pos, current_node, move)
                child_node.heuristic_cost = child_heuristic_cost
                children.append(child_node)
                
        if children:
            current_node = min(children, key=lambda x: x.heuristic_cost)
            can_continue = True
            
        if current_node.floor_state == GOAL_STATE:
            return generate_path_list(current_node, True)
            
        if not can_continue:
            return generate_path_list(current_node, False)
#
#=============================================================================
#Leo đồi ngẫu nhiên + restart max
#
def run_random_restart_hill_climbing(floor, vacuum_pos, max_restart: int):
    #max_restart được mặc định khai báo là 10
    current_node = Node(floor_state=floor, position=vacuum_pos, parent=None, birth_action=None)
    current_node.heuristic_cost = get_heuristic_cost(floor, vacuum_pos)
    step = 0
    loop_counter = 0
    
    if floor == GOAL_STATE:
        return generate_path_list(current_node, True)
    
    while loop_counter < max_restart:
        step += 1
        moves = posible_moves(current_node.position)
        children = []
        
        for move in moves:
            temp_floor, temp_vacuum_pos = apply_move(current_node.floor_state, current_node.position, move)
            child_heuristic_cost = get_heuristic_cost(temp_floor, temp_vacuum_pos)
            
            if child_heuristic_cost < current_node.heuristic_cost:
                child_node = Node(floor_state=temp_floor, position=temp_vacuum_pos, parent=current_node, birth_action=move)
                child_node.heuristic_cost = child_heuristic_cost
                children.append(child_node)
                
        if children:
            current_node = random.choice(children)
        else:
            # Restart từ trạng thái ban đầu
            current_node = Node(floor_state=floor, position=vacuum_pos, parent=None, birth_action=None)
            current_node.heuristic_cost = get_heuristic_cost(floor, vacuum_pos)
            loop_counter += 1
            continue
        
        if current_node.floor_state == GOAL_STATE:
            return generate_path_list(current_node, True)
        
    return generate_path_list(current_node, False)

#=============================================================================
# Local Beam Search - Lọc trùng nội bộ thế hệ con (Local Filtering)
#
def run_local_beam_search_local_filtering(floor, vacuum_pos, k=2):
    root = Node(floor_state=floor, position=vacuum_pos, parent=None, birth_action=None)
    root.heuristic_cost = get_heuristic_cost(floor, vacuum_pos)
    
    if floor == GOAL_STATE:
        return generate_path_list(root, True)
        
    started_moves = posible_moves(vacuum_pos)
    current_nodes = []
    
    for move in started_moves:
        temp_floor, temp_pos = apply_move(floor, vacuum_pos, move)
        temp_node = Node(floor_state=temp_floor, position=temp_pos, parent=root, birth_action=move)
        temp_node.heuristic_cost = get_heuristic_cost(temp_floor, temp_pos)
        
        if temp_floor == GOAL_STATE:
            return generate_path_list(temp_node, True)
        current_nodes.append(temp_node)
        
    if not current_nodes:
        return generate_path_list(root, False)
        
    max_steps = 1000
    step = 0
    while step < max_steps:
        step += 1
        neighbors_states = []
        seen_in_generation = set()
        
        for node in current_nodes:
            neigh_possible_moves = posible_moves(node.position)
            
            for move in neigh_possible_moves:
                neigh_floor, neigh_vacuum_pos = apply_move(node.floor_state, node.position, move)
                
                floor_tuple = tuple(tuple(row) for row in neigh_floor)
                state_key = (floor_tuple, neigh_vacuum_pos)
                
                if state_key not in seen_in_generation:
                    seen_in_generation.add(state_key)
                    neigh_node = Node(floor_state=neigh_floor, position=neigh_vacuum_pos, parent=node, birth_action=move)
                    neigh_node.heuristic_cost = get_heuristic_cost(neigh_floor, neigh_vacuum_pos)
                    
                    if neigh_floor == GOAL_STATE:
                        return generate_path_list(neigh_node, True)
                    
                    neighbors_states.append(neigh_node)
                    
        if not neighbors_states:
            break
            
        neighbors_states.sort(key=lambda x: x.heuristic_cost)
        current_nodes = neighbors_states[:k]
        
    best_node = min(current_nodes, key=lambda x: x.heuristic_cost)
    return generate_path_list(best_node, False)
#=============================================================================
# Simulated Annealing
#
def run_simulated_annealing(floor, vacuum_pos):
    current_node = Node(floor, vacuum_pos, None, None)
    current_node.heuristic_cost = get_heuristic_cost(floor, vacuum_pos)
    step = 0
    t = 100
    t_min = 0.1
    alpha = 0.95
    
    while t > t_min:
        if current_node.floor_state == GOAL_STATE:
            return generate_path_list(current_node, True)
        
        step += 1
        moves = posible_moves(current_node.position)
        neighbors = []
        for move in moves:
            neigh_floor, neigh_pos = apply_move(current_node.floor_state, current_node.position, move)
            neigh = Node(neigh_floor, neigh_pos, current_node, move)
            neigh.heuristic_cost = get_heuristic_cost(neigh_floor, neigh_pos)
            neighbors.append(neigh)

        next_node = random.choice(neighbors)
        delta = next_node.heuristic_cost - current_node.heuristic_cost
        if current_node.heuristic_cost > next_node.heuristic_cost:
            current_node = next_node
        else:
            p = math.exp(-delta / t)
            if random.uniform(0,1) < p:
                current_node = next_node
        t = alpha * t
    
    return generate_path_list(current_node, False)