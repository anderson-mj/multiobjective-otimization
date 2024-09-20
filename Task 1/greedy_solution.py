def load(filename):
    with open(filename, 'r') as f:
        n = int(f.readline().strip())
        Q = int(f.readline().strip())
        profits = list(map(int, f.readline().strip().split()))
        weights = list(map(int, f.readline().strip().split()))
    
    return n, Q, profits, weights

def greedy_solution(n, Q, profits, weights):
    ratio = [(profits[i] / weights[i], i) for i in range(n)]
    ratio.sort(reverse=True, key=lambda x: x[0])
    
    total_weight = 0
    total_profit = 0
    solution = [0] * n
    
    for r, i in ratio:
        if total_weight + weights[i] <= Q:
            solution[i] = 1
            total_weight += weights[i]
            total_profit += profits[i]
    
    return solution, total_profit

n, Q, profits, weights = load('knapsack_data.txt')
solution, total_profit = greedy_solution(n, Q, profits, weights)
print(f"Greedy solution: {solution}")
print(f"Total profit: {total_profit}")