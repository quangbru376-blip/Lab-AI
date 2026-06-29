# Adversarial Search Algorithms

Đây là mã giả (Pseudo-code) cho các thuật toán tìm kiếm đối kháng, dùng trong các trò chơi đối kháng có tổng bằng 0 (như Tic-Tac-Toe, Cờ vua).

## 1. Minimax Algorithm
```text
function MINIMAX-DECISION(state) returns an action
    return argmax a in ACTIONS(state) MIN-VALUE(RESULT(state, a))

function MAX-VALUE(state) returns a utility value
    if TERMINAL-TEST(state) then return UTILITY(state)
    v = -∞
    for each a in ACTIONS(state) do
        v = MAX(v, MIN-VALUE(RESULT(state, a)))
    return v

function MIN-VALUE(state) returns a utility value
    if TERMINAL-TEST(state) then return UTILITY(state)
    v = +∞
    for each a in ACTIONS(state) do
        v = MIN(v, MAX-VALUE(RESULT(state, a)))
    return v
```

## 2. Alpha-Beta Pruning
```text
function ALPHA-BETA-SEARCH(state) returns an action
    v = MAX-VALUE(state, -∞, +∞)
    return the action in ACTIONS(state) with value v

function MAX-VALUE(state, α, β) returns a utility value
    if TERMINAL-TEST(state) then return UTILITY(state)
    v = -∞
    for each a in ACTIONS(state) do
        v = MAX(v, MIN-VALUE(RESULT(state, a), α, β))
        if v ≥ β then return v
        α = MAX(α, v)
    return v

function MIN-VALUE(state, α, β) returns a utility value
    if TERMINAL-TEST(state) then return UTILITY(state)
    v = +∞
    for each a in ACTIONS(state) do
        v = MIN(v, MAX-VALUE(RESULT(state, a), α, β))
        if v ≤ α then return v
        β = MIN(β, v)
    return v
```

## 3. Expectimax Algorithm
Dành cho các môi trường có yếu tố ngẫu nhiên (hoặc đối thủ chơi ngẫu nhiên/không tối ưu).
```text
function EXPECTIMAX(state) returns a utility value
    if TERMINAL-TEST(state) then return UTILITY(state)
    if state is a MAX node then return MAX-VALUE(state)
    if state is a CHANCE node then return EXPECTED-VALUE(state)

function MAX-VALUE(state) returns a utility value
    v = -∞
    for each a in ACTIONS(state) do
        v = MAX(v, EXPECTIMAX(RESULT(state, a)))
    return v

function EXPECTED-VALUE(state) returns a utility value
    v = 0
    for each a in ACTIONS(state) do
        p = PROBABILITY(state, a)
        v = v + p * EXPECTIMAX(RESULT(state, a))
    return v
```
