# 🤖 AI Algorithms & Visualizers 🚀

Chào mừng bạn đến với kho lưu trữ tổng hợp các **Thuật toán Trí tuệ Nhân tạo (AI)** được viết hoàn toàn bằng Python! 🐍 
Đặc biệt, repo này cung cấp các **Visualizers (Trình trực quan hóa)** cực kỳ sinh động để giúp bạn "mắt thấy tai nghe" cách các thuật toán AI hoạt động trong thực tế. Toàn bộ các thuật toán ở đây đều được đúc kết từ môn học Trí tuệ Nhân tạo. 💡

### Giảng viên hướng dẫn: Tiến sĩ. Phan Thị Thùy Trang
### Tên tác giả: Đặng Duy Quang
### MSSV tác giả: 24110307
---

## 🎨 Khám phá Các Trình Trực Quan Hoá (Visualizers)

Học AI sẽ không hề khô khan nếu bạn có thể nhìn thấy chúng chuyển động! Dưới đây là 3 "vũ khí" trực quan chính trong repo này:

### 1. 🖍️ Coloring Visualizer (`Coloring_Visualizer`)
Bạn đau đầu với bài toán **Thoả mãn Ràng buộc (CSP)**? Visualizer này sẽ biến việc **Tô màu đồ thị (Graph Coloring)** thành một buổi trình diễn nghệ thuật! 🎨
- **Nhiệm vụ:** Tô màu các đỉnh sao cho không có 2 đỉnh kề nhau nào bị "đụng hàng" màu sắc.
- **Thuật toán áp dụng:** Bạn sẽ được tận mắt quan sát cách AI "thử và sai" hay "tiên đoán" thông qua các thuật toán: `Backtracking` (Quay lui), `Forward Checking` (Kiểm tra tới) và `Min Conflicts` (Tối thiểu hóa xung đột).

![Demo Coloring Visualizer](https://github.com/quangbru376-blip/Lab-AI/blob/main/gif/Coloring.gif)

---

### 2. ⚔️ Tic-Tac-Toe Visualizer (`Tictactoe_Visualizer`)
Đưa bạn vào đấu trường trí tuệ của bộ môn **Tìm kiếm đối kháng (Adversarial Search)**! 🎮
- **Trải nghiệm:** Xem một "bộ não AI" tính toán hàng nghìn nước đi trước khi đánh dấu X hay O. 
- **Thuật toán áp dụng:** Đi sâu vào cây trò chơi với các "tuyệt chiêu" như `Minimax` (tính toán hoàn hảo), `Alpha-Beta Pruning` (cắt tỉa thông minh để suy nghĩ nhanh hơn) và `Expectimax` (đối phó với những biến số khó lường). 🧠

![Demo Tic Tac Toe Visualizer](https://github.com/quangbru376-blip/Lab-AI/blob/main/gif/Tictactoe.gif)

---

### 3. 🧹 Vacuum Cleaner Visualizer (`Vacuum_Cleaner_Visualizer`)
Theo chân một "chuyên gia dọn dẹp" (tác nhân máy hút bụi AI) rong ruổi khắp bản đồ lưới để dọn sạch bụi bẩn! ✨
- **Môi trường:** Đa dạng từ thế giới tất định (biết mọi thứ), quan sát một phần cho đến thế giới hoàn toàn ngẫu nhiên.
- **Thuật toán áp dụng:** Nơi hội tụ của các thuật toán tìm kiếm không gian trạng thái kinh điển: từ dò dẫm cơ bản (`BFS`, `DFS`), dò tìm có tính toán (`UCS`, `A*`) cho đến các thuật toán xử lý môi trường bất định và phức tạp. Nhìn AI dọn dẹp đảm bảo cực kỳ thỏa mãn! 🤖✨

![Demo Vacuum Visualizer](https://github.com/quangbru376-blip/Lab-AI/blob/main/gif/Vacuum.gif)

---

## Algorithms Pseudocode

Below are the pseudocodes for the AI algorithms used and studied in this repository, categorized by their respective domains.

### 1. Uninformed Search

**BFS (Breadth-First Search)**
```python
def BFS(problem):
    node = Node(state=problem.initial_state)
    if problem.is_goal(node.state): return node
    frontier = Queue([node]) # Hàng đợi FIFO
    explored = Set()
    while not frontier.is_empty():
        node = frontier.pop()
        explored.add(node.state)
        for action in problem.actions(node.state):
            child = child_node(problem, node, action)
            if child.state not in explored and child.state not in frontier:
                if problem.is_goal(child.state): return child
                frontier.push(child)
    return None
```

**DFS (Depth-First Search)**
```python
def DFS(problem):
    frontier = Stack([Node(state=problem.initial_state)]) # Ngăn xếp LIFO
    explored = Set()
    while not frontier.is_empty():
        node = frontier.pop()
        if problem.is_goal(node.state): return node
        if node.state not in explored:
            explored.add(node.state)
            for action in problem.actions(node.state):
                frontier.push(child_node(problem, node, action))
    return None
```

**UCS (Uniform-Cost Search)**
```python
def UCS(problem):
    node = Node(state=problem.initial_state)
    frontier = PriorityQueue(node, key=lambda n: n.path_cost) # Hàng đợi ưu tiên theo g(n)
    explored = Set()
    while not frontier.is_empty():
        node = frontier.pop() # Lấy nút có chi phí g(n) nhỏ nhất
        if problem.is_goal(node.state): return node
        explored.add(node.state)
        for action in problem.actions(node.state):
            child = child_node(problem, node, action)
            if child.state not in explored and child.state not in frontier:
                frontier.push(child)
            elif child.state in frontier với chi phí cao hơn:
                thay thế nút đó trong frontier bằng child
    return None
```

### 2. Informed Search

**Greedy Best-First Search**
```python
def Greedy_Best_First(problem):
    node = Node(state=problem.initial_state)
    frontier = PriorityQueue(node, key=lambda n: heuristic(n.state)) # Theo h(n)
    explored = Set()
    while not frontier.is_empty():
        node = frontier.pop()
        if problem.is_goal(node.state): return node
        explored.add(node.state)
        for action in problem.actions(node.state):
            child = child_node(problem, node, action)
            if child.state not in explored and child.state not in frontier:
                frontier.push(child)
    return None
```

**A* Search**
```python
def A_Star(problem):
    node = Node(state=problem.initial_state)
    # Sắp xếp theo f(n) = g(n) + h(n)
    frontier = PriorityQueue(node, key=lambda n: n.path_cost + heuristic(n.state))
    explored = Set()
    while not frontier.is_empty():
        node = frontier.pop()
        if problem.is_goal(node.state): return node
        explored.add(node.state)
        for action in problem.actions(node.state):
            child = child_node(problem, node, action)
            if child.state not in explored and child.state not in frontier:
                frontier.push(child)
            elif child.state in frontier với f(n) lớn hơn:
                thay thế nút đó trong frontier bằng child
    return None
```

**IDA* (Iterative Deepening A*)**
```python
def IDA_Star(problem):
    node = Node(state=problem.initial_state, path_cost=0)
    limit = node.path_cost + heuristic(node.state) # f(n) ban đầu
    while True:
        result, next_limit = search(problem, node, limit)
        if result == "Found": return solution_path
        if result == "No solution": return None
        limit = next_limit # Tăng ngưỡng cắt bằng f(n) nhỏ nhất vượt ngưỡng

def search(problem, node, limit):
    f_n = node.path_cost + heuristic(node.state)
    if f_n > limit: return "Cutoff", f_n
    if problem.is_goal(node.state): return "Found", limit
    
    min_exceeded = infinity
    for action in problem.actions(node.state):
        child = child_node(problem, node, action)
        result, next_limit = search(problem, child, limit)
        if result == "Found": return "Found", limit
        if result == "Cutoff": 
            min_exceeded = min(min_exceeded, next_limit)
    
    if min_exceeded == infinity:
        return "No solution", limit
    return "Cutoff", min_exceeded
```

### 3. Adversarial Search

**Minimax**
```python
def Minimax_Decision(state):
    return argmax(actions, key=lambda a: Min_Value(Result(state, a)))

def Max_Value(state):
    if Terminal_Test(state): return Utility(state)
    v = -infinity
    for action in Actions(state):
        v = max(v, Min_Value(Result(state, action)))
    return v

def Min_Value(state):
    if Terminal_Test(state): return Utility(state)
    v = infinity
    for action in Actions(state):
        v = min(v, Max_Value(Result(state, action)))
    return v
```

**Alpha-Beta Pruning**
```python
def Alpha_Beta_Search(state):
    v = Max_Value(state, -infinity, +infinity)
    return action_leading_to_v

def Max_Value(state, alpha, beta):
    if Terminal_Test(state): return Utility(state)
    v = -infinity
    for action in Actions(state):
        v = max(v, Min_Value(Result(state, action), alpha, beta))
        if v >= beta: return v
        alpha = max(alpha, v)
    return v

def Min_Value(state, alpha, beta):
    if Terminal_Test(state): return Utility(state)
    v = +infinity
    for action in Actions(state):
        v = min(v, Max_Value(Result(state, action), alpha, beta))
        if v <= alpha: return v
        beta = min(beta, v)
    return v
```

**Expectimax**
```python
def Expectimax_Decision(state):
    return argmax(actions, key=lambda a: Expect_Value(Result(state, a)))

def Expect_Value(state):
    if Terminal_Test(state): return Utility(state)
    v = 0
    actions = Actions(state)
    probability = 1.0 / len(actions) # Phân phối xác suất đều của đối thủ ngẫu nhiên
    for action in actions:
        v += probability * Max_Value(Result(state, action))
    return v
```

### 4. Local Search

**Simple Hill Climbing**
```python
def Simple_Hill_Climbing(problem):
    current = problem.initial_state
    
    while True:
        neighbors = problem.neighbors(current)
        found_better = False
        
        for neighbor in neighbors:
            if value(neighbor) > value(current):
                current = neighbor
                found_better = True
                break

        if not found_better:
            return current
```

**Beam Search**
```python
def Beam_Search(problem, k):
    frontier = [problem.initial_state]
    while not goal_found:
        candidates = []
        for state in frontier:
            candidates.extend(problem.neighbors(state))
        frontier = select_best_k(candidates, k) # Giữ lại k trạng thái tốt nhất
        if goal in frontier: return goal
    return None
```

**Simulated Annealing**
```python
def Simulated_Annealing(problem, schedule):
    current = problem.initial_state
    for t in range(1, infinity):
        T = schedule(t) # Nhiệt độ giảm dần
        if T == 0: return current
        next_state = random_select(problem.neighbors(current))
        delta_E = value(next_state) - value(current)
        if delta_E > 0:
            current = next_state
        else:
            # Chấp nhận trạng thái tệ hơn với xác suất e^(delta_E / T)
            current = next_state with probability e^(delta_E / T)
```

### 5. Constraint Satisfaction Problems (CSP)

**Backtracking Search**
```python
def Backtracking_Search(csp):
    return Backtrack({}, csp)

def Backtrack(assignment, csp):
    if is_complete(assignment, csp): return assignment
    var = select_unassigned_variable(assignment, csp)
    for value in order_domain_values(var, assignment, csp):
        if is_consistent(var, value, assignment, csp):
            assignment.add(var, value)
            result = Backtrack(assignment, csp)
            if result != failure: return result
            assignment.remove(var, value)
    return failure
```

**Forward Checking**
```python
def Forward_Checking(assignment, csp, var, value):
    assignment.add(var, value)
    for neighbor in csp.neighbors(var):
        if neighbor not in assignment:
            remove value from neighbor.domain if it violates constraints
            if neighbor.domain is empty:
                return failure
    return success
```

**Min Conflicts**
```python
def Min_Conflicts(csp, max_steps):
    assignment = random_assignment(csp)
    for i in range(max_steps):
        if assignment.is_complete(): return assignment
        var = conflicted_variable(assignment, csp)
        value = argmin(csp.domain[var], lambda val: count_conflicts(var, val, assignment, csp))
        assignment.add(var, value)
    return failure
```

### 6. Complex Environments

**Sensorless Search (Belief State Search with BFS)**
```python
def Sensorless_Search(problem):
    # problem.initial_state là một tập hợp (belief state) gồm các physical states
    # Ví dụ: { state1, state2, state3, state4 }
    belief_node = Node(state=problem.initial_state)
    
    if problem.is_goal(belief_node.state): 
        return belief_node
        
    frontier = Queue([belief_node])
    explored = Set()
    
    while not frontier.is_empty():
        belief_node = frontier.pop()
        explored.add(belief_node.state)
        
        for action in problem.actions(belief_node.state):
            # child_belief_state được tạo bằng cách áp dụng action lên MỌI physical state trong belief_node.state
            child_belief = child_node(problem, belief_node, action)
            
            if child_belief.state not in explored and child_belief.state not in frontier:
                if problem.is_goal(child_belief.state): 
                    return child_belief
                frontier.push(child_belief)
                
    return None
```

**Partially Observable Search (Multiverse BFS)**
```python
def Partially_Observable_Search(problem):
    # Khởi tạo tập hợp tất cả các trạng thái có thể có ban đầu (Belief state / Multiverses)
    belief_state = problem.initial_belief_state()
    
    # Kế hoạch hành động rỗng
    plan = []
    
    while not problem.is_goal(problem.true_state):
        # Lấy thông tin cảm biến từ môi trường thật
        percept = problem.get_percept(problem.true_state)
        
        # Cập nhật belief_state: Loại bỏ các trạng thái không khớp với percept
        belief_state = problem.update_belief_state(belief_state, percept)
        
        # Dùng BFS tìm đường đi từ true_state tới mục tiêu (xu gần nhất)
        path = BFS(problem.true_state, problem.goal)
        
        if not path:
            return "Failure"
            
        # Thực thi hành động đầu tiên trong kế hoạch tìm được
        action = path[0]
        plan.append(action)
        
        # Cập nhật true_state sau khi thực hiện hành động
        problem.true_state = problem.result(problem.true_state, action)
        
        # Cập nhật tất cả các trạng thái trong belief_state theo action đó
        belief_state = problem.predict_belief_state(belief_state, action)
        
    return plan
```

**And-Or Graph Search**
```python
def And_Or_Graph_Search(problem):
    return Or_Search(problem.initial_state, problem, [])

def Or_Search(state, problem, path):
    if problem.is_goal(state): 
        return []
    if state in path: 
        return "Failure"
        
    for action in problem.actions(state):
        # Lấy tất cả các kết quả có thể xảy ra từ môi trường không tất định (AND node)
        results = problem.results(state, action)
        
        # Gọi And_Search để xem hành động này có dẫn tới đích trong mọi trường hợp không
        plan = And_Search(results, problem, path + [state])
        
        if plan != "Failure":
            return [action, plan]
            
    return "Failure"

def And_Search(states, problem, path):
    plan = {}
    for state in states:
        # Gọi đệ quy Or_Search cho từng trạng thái kết quả có thể xảy ra
        sub_plan = Or_Search(state, problem, path)
        if sub_plan == "Failure":
            return "Failure"
        plan[state] = sub_plan
    return plan
```
