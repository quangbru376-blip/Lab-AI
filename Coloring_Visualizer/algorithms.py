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