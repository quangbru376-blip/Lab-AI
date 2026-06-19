import copy
import random

constrains = {
    "Thành phố Thủ Đức": [
        "Quận 1", "Quận 4", "Quận 7", "Quận 12", "Quận Bình Thạnh"],
    "Quận 1": [
        "Thành phố Thủ Đức", "Quận 3", "Quận 4", "Quận 5", "Quận Bình Thạnh", "Quận Phú Nhuận"],
    "Quận 3": [
        "Quận 1", "Quận 5", "Quận 10", "Quận Phú Nhuận", "Quận Tân Bình"],
    "Quận 4": [
        "Thành phố Thủ Đức", "Quận 1", "Quận 5", "Quận 7", "Quận 8"],
    "Quận 5": [
        "Quận 1", "Quận 3", "Quận 4", "Quận 6", "Quận 8", "Quận 10", "Quận 11"],
    "Quận 6": [
        "Quận 5", "Quận 8", "Quận 11", "Quận Bình Tân", "Quận Tân Phú"],
    "Quận 7": [
        "Thành phố Thủ Đức", "Quận 4", "Quận 8", "Huyện Bình Chánh", "Huyện Nhà Bè"],
    "Quận 8": [
        "Quận 4", "Quận 5", "Quận 6", "Quận 7", "Quận Bình Tân", "Huyện Bình Chánh"],
    "Quận 10": [
        "Quận 3", "Quận 5", "Quận 11", "Quận Tân Bình"],
    "Quận 11": [
        "Quận 5", "Quận 6", "Quận 10", "Quận Tân Bình", "Quận Tân Phú"],
    "Quận 12": [
        "Thành phố Thủ Đức", "Quận Bình Tân", "Quận Gò Vấp", "Quận Bình Thạnh", "Quận Tân Bình", "Huyện Hóc Môn"],
    "Quận Bình Thạnh": [
        "Thành phố Thủ Đức", "Quận 1", "Quận 12", "Quận Gò Vấp", "Quận Phú Nhuận"],
    "Quận Gò Vấp": [
        "Quận 12", "Quận Bình Thạnh", "Quận Phú Nhuận", "Quận Tân Bình"],
    "Quận Phú Nhuận": [
        "Quận 1", "Quận 3", "Quận Bình Thạnh", "Quận Gò Vấp", "Quận Tân Bình"],
    "Quận Tân Bình": [
        "Quận 3", "Quận 10", "Quận 11", "Quận 12", "Quận Gò Vấp", "Quận Phú Nhuận", "Quận Tân Phú"],
    "Quận Tân Phú": [
        "Quận 6", "Quận 11", "Quận Tân Bình", "Quận Bình Tân"],
    "Quận Bình Tân": [
        "Quận 6", "Quận 8", "Quận 12", "Quận Tân Phú", "Huyện Bình Chánh", "Huyện Hóc Môn"],
    "Huyện Bình Chánh": [
        "Quận 7", "Quận 8", "Quận Bình Tân", "Huyện Hóc Môn", "Huyện Nhà Bè"],
    "Huyện Hóc Môn": [
        "Quận 12", "Quận Bình Tân", "Huyện Bình Chánh", "Huyện Củ Chi"],
    "Huyện Củ Chi": [
        "Huyện Hóc Môn"],
    "Huyện Nhà Bè": [
        "Quận 7", "Huyện Bình Chánh", "Huyện Cần Giờ"],
    "Huyện Cần Giờ": [
        "Huyện Nhà Bè"]
}

COLOR = ["Đỏ", "Cam", "Vàng", "Lục", "Lam", "Đen", "Trắng"]

# Initialize assignments for all districts
assignments = {district: None for district in constrains.keys()}
list_of_keys = list(constrains.keys())

def is_same_color_as_neighbors(district, color):
    for key in constrains[district]:
        if color == assignments[key]:
            return True
    return False

def backtracking_coloring(assignment_index: int):
    # Base case: if all districts are colored, return True
    if assignment_index >= len(constrains):
        return True
    
    current_key = list_of_keys[assignment_index]
    
    for color in COLOR:
        if not is_same_color_as_neighbors(current_key, color):
            # Try assigning color
            assignments[current_key] = color
            
            # Recurse
            if backtracking_coloring(assignment_index + 1):
                return True
            
            # Backtrack
            assignments[current_key] = None
            
    return False

def backtracking_coloring_generator(constrains, colors_list, list_of_keys, assignments, idx=0):
    # Base case: if all districts are colored, return True
    if idx >= len(list_of_keys):
        yield ("SUCCESS", None, None, None)
        return True
    
    node = list_of_keys[idx]
    
    for color in colors_list:
        # 1. Yield checking/trying action
        yield ("TRYING", node, color, None)
        
        # Check for same color as adjacent neighbors
        conflicts = []
        for neighbor in constrains[node]:
            if assignments.get(neighbor) == color:
                conflicts.append(neighbor)
        
        # 2. Yield conflict if found
        if conflicts:
            yield ("CONFLICT", node, color, conflicts)
            continue
        
        # 3. Assign color and yield assignment
        assignments[node] = color
        yield ("ASSIGN", node, color, None)
        
        # Recurse for the next index
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
        
        # 4. If search failed, backtrack (reset color) and yield backtrack
        assignments[node] = None
        yield ("BACKTRACK", node, color, None)
        
    return False


def forward_checking_generator(constrains, colors_list, list_of_keys, assignments, present_domain=None, idx=0):
    if present_domain is None:
        present_domain = {district: list(colors_list) for district in list_of_keys}
        
    if idx >= len(list_of_keys):
        yield ("SUCCESS", None, None, None)
        return True
        
    node = list_of_keys[idx]
    for color in present_domain[node]:
        yield ("TRYING", node, color, None)
        
        temp_domain = copy.deepcopy(present_domain)
        conflicts = []
        fc_fail = False
        
        for neighbor in constrains[node]:
            if assignments.get(neighbor) is None:  # Chỉ lọc miền giá trị láng giềng chưa gán màu
                if color in temp_domain[neighbor]:
                    temp_domain[neighbor].remove(color)
                if len(temp_domain[neighbor]) == 0:
                    conflicts.append(neighbor)
                    fc_fail = True
        
        if fc_fail:
            yield ("CONFLICT", node, color, conflicts)
            continue
            
        assignments[node] = color
        yield ("ASSIGN", node, color, None)
        
        sub_gen = forward_checking_generator(constrains, colors_list, list_of_keys, assignments, temp_domain, idx + 1)
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


def min_conflicts_generator(constrains, colors_list, list_of_keys, assignments, max_steps=1000):
    # Khởi tạo gán màu ngẫu nhiên cho tất cả các quận (Complete Assignment)
    for node in list_of_keys:
        color = random.choice(colors_list)
        assignments[node] = color
        yield ("ASSIGN", node, color, None)
        
    for step in range(max_steps):
        # Tìm các quận bị xung đột màu với láng giềng
        conflicted_nodes = []
        for node in list_of_keys:
            conflicts = []
            for neighbor in constrains[node]:
                if assignments.get(neighbor) == assignments[node]:
                    conflicts.append(neighbor)
            if conflicts:
                conflicted_nodes.append((node, conflicts))
        
        # Nếu không còn quận nào bị xung đột, ta đã tìm thấy lời giải hợp lệ
        if not conflicted_nodes:
            yield ("SUCCESS", None, None, None)
            return True
            
        # Chọn ngẫu nhiên một quận bị xung đột
        node, conflicts = random.choice(conflicted_nodes)
        yield ("CONFLICT", node, assignments[node], conflicts)
        
        # Tìm màu có số lượng xung đột ít nhất cho quận này
        min_conflict_count = float('inf')
        best_colors = []
        for color in colors_list:
            count = 0
            for neighbor in constrains[node]:
                if assignments.get(neighbor) == color:
                    count += 1
            if count < min_conflict_count:
                min_conflict_count = count
                best_colors = [color]
            elif count == min_conflict_count:
                best_colors.append(color)
        
        # Gán màu được chọn ngẫu nhiên trong danh sách các màu tối ưu nhất
        color = random.choice(best_colors)
        assignments[node] = color
        yield ("ASSIGN", node, color, None)
        
    return False


def revise(present_domain, xi, xj, constrains):
    revised = False
    for color_i in list(present_domain[xi]):
        has_support = False
        for color_j in present_domain[xj]:
            if color_i != color_j:
                has_support = True
                break
        if not has_support:
            present_domain[xi].remove(color_i)
            revised = True
    return revised


def ac3(present_domain, constrains):
    queue = []
    for xi in constrains.keys():
        for xj in constrains[xi]:
            queue.append((xi, xj))
            
    while queue:
        (xi, xj) = queue.pop(0)
        if revise(present_domain, xi, xj, constrains):
            if len(present_domain[xi]) == 0:
                return False
            for xk in constrains[xi]:
                if xk != xj:
                    queue.append((xk, xi))
    return True


def ac3_coloring_generator(constrains, colors_list, list_of_keys, assignments, present_domain=None, idx=0):
    if present_domain is None:
        present_domain = {district: list(colors_list) for district in list_of_keys}
        
    if idx >= len(list_of_keys):
        yield ("SUCCESS", None, None, None)
        return True
        
    node = list_of_keys[idx]
    for color in present_domain[node]:
        yield ("TRYING", node, color, None)
        
        temp_domain = copy.deepcopy(present_domain)
        temp_domain[node] = [color]
        
        if ac3(temp_domain, constrains):
            assignments[node] = color
            yield ("ASSIGN", node, color, None)
            
            sub_gen = ac3_coloring_generator(constrains, colors_list, list_of_keys, assignments, temp_domain, idx + 1)
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
        else:
            # Tìm láng giềng có miền giá trị bị rỗng để hiển thị xung đột
            empty_nodes = [n for n in list_of_keys if len(temp_domain[n]) == 0]
            yield ("CONFLICT", node, color, empty_nodes)
            
    return False


# Run backtracking coloring starting from index 0
if __name__ == "__main__":
    if backtracking_coloring(0):
        print("Tìm thấy lời giải tô màu các quận:")
        print("---------------------------------")
        for district, color in assignments.items():
            print(f"{district:25} -> {color}")
        print("---------------------------------")
        
        # Verify the results to be absolutely sure
        valid = True
        for district, neighbors in constrains.items():
            for neighbor in neighbors:
                if assignments[district] == assignments[neighbor]:
                    print(f"LỖI: {district} và {neighbor} cùng màu {assignments[district]}!")
                    valid = False
        if valid:
            print("Xác nhận: Tất cả các quận kề nhau đều khác màu nhau (Hợp lệ).")
    else:
        print("Không tìm thấy lời giải với các màu đã cho.")