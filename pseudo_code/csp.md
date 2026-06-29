# Constraint Satisfaction Problem (CSP) Algorithms

Đây là mã giả (Pseudo-code) cho các thuật toán giải quyết bài toán thỏa mãn ràng buộc (CSP), ví dụ như bài toán tô màu bản đồ.

## 1. Backtracking Search (Tìm kiếm quay lui)
```text
function BACKTRACKING-SEARCH(csp) returns a solution, or failure
    return BACKTRACK({}, csp)

function BACKTRACK(assignment, csp) returns a solution, or failure
    if assignment is complete then return assignment
    var = SELECT-UNASSIGNED-VARIABLE(csp)
    for each value in ORDER-DOMAIN-VALUES(var, assignment, csp) do
        if value is consistent with assignment then
            add {var = value} to assignment
            inferences = INFERENCE(csp, var, value)
            if inferences != failure then
                add inferences to assignment
                result = BACKTRACK(assignment, csp)
                if result != failure then
                    return result
            remove {var = value} and inferences from assignment
    return failure
```

## 2. Forward Checking
Forward checking là một phương pháp inference kết hợp trong quá trình backtracking.
```text
function FORWARD-CHECKING(csp, var, value, assignment) returns inferences, or failure
    inferences = {}
    for each unassigned variable Y that is connected to var by a constraint do
        remove value from Y's domain
        if Y's domain is empty then
            return failure
        else
            add {Y's updated domain} to inferences
    return inferences
```
*Ghi chú: Thường được gọi trong hàm INFERENCE của Backtracking ở trên.*

## 3. AC-3 (Arc Consistency 3)
```text
function AC-3(csp) returns false if an inconsistency is found and true otherwise
    queue = a queue of arcs, initially all the arcs in csp
    while queue is not empty do
        (Xi, Xj) = REMOVE-FIRST(queue)
        if REVISE(csp, Xi, Xj) then
            if size of Di == 0 then return false
            for each Xk in Xi.NEIGHBORS - {Xj} do
                add (Xk, Xi) to queue
    return true

function REVISE(csp, Xi, Xj) returns true iff we revise the domain of Xi
    revised = false
    for each x in Di do
        if no value y in Dj allows (x,y) to satisfy the constraint between Xi and Xj then
            delete x from Di
            revised = true
    return revised
```

## 4. Min-Conflicts (Local Search)
```text
function MIN-CONFLICTS(csp, max_steps) returns a solution or failure
    current = an initial complete assignment for csp
    for i = 1 to max_steps do
        if current is a solution for csp then return current
        var = a randomly chosen conflicted variable from csp.VARIABLES
        value = the value v for var that minimizes CONFLICTS(var, v, current, csp)
        set var = value in current
    return failure
```
