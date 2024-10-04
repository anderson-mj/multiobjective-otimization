import random
import time

def load(filename):
    with open(filename, 'r') as f:
        n = int(f.readline().strip())
        Q = int(f.readline().strip())
        profits = list(map(int, f.readline().strip().split()))
        weights = list(map(int, f.readline().strip().split()))
    
    return n, Q, profits, weights

def generate_initial_solution(n):
    return [random.choice([0, 1]) for _ in range(n)]

def evaluate_solution(solution, profits, weights, Q):
    total_weight = sum(w for w, s in zip(weights, solution) if s)
    total_profit = sum(p for p, s in zip(profits, solution) if s)
    if total_weight > Q:
        return 0  # Infeasible solution
    return total_profit

def get_neighbors(solution):
    neighbors = []
    for i in range(len(solution)):
        neighbor = solution[:]
        neighbor[i] = 1 - neighbor[i]  # Flip the bit
        neighbors.append(neighbor)
    return neighbors

def best_improvement(solution, profits, weights, Q):
    best_solution = solution
    best_value = evaluate_solution(solution, profits, weights, Q)
    for neighbor in get_neighbors(solution):
        neighbor_value = evaluate_solution(neighbor, profits, weights, Q)
        if neighbor_value > best_value:
            best_solution = neighbor
            best_value = neighbor_value
    return best_solution, best_value

def first_improvement(solution, profits, weights, Q):
    for neighbor in get_neighbors(solution):
        neighbor_value = evaluate_solution(neighbor, profits, weights, Q)
        if neighbor_value > evaluate_solution(solution, profits, weights, Q):
            return neighbor, neighbor_value
    return solution, evaluate_solution(solution, profits, weights, Q)

def local_search(profits, weights, Q, iterations=1000000):
    n = len(profits)
    best_solutions_bi = []
    best_solutions_fi = []
    start_time_bi = time.time()
    for _ in range(iterations):
        initial_solution = generate_initial_solution(n)
        best_solution_bi, best_value_bi = best_improvement(initial_solution, profits, weights, Q)
        best_solutions_bi.append(best_value_bi)
    end_time_bi = time.time()
    
    start_time_fi = time.time()
    for _ in range(iterations):
        initial_solution = generate_initial_solution(n)
        best_solution_fi, best_value_fi = first_improvement(initial_solution, profits, weights, Q)
        best_solutions_fi.append(best_value_fi)
    end_time_fi = time.time()
    
    avg_cost_bi = sum(best_solutions_bi) / iterations
    avg_cost_fi = sum(best_solutions_fi) / iterations
    time_bi = end_time_bi - start_time_bi
    time_fi = end_time_fi - start_time_fi
    
    return avg_cost_bi, time_bi, avg_cost_fi, time_fi

if __name__ == "__main__":
    n, Q, profits, weights = load('knapsack_data.txt')
    avg_cost_bi, time_bi, avg_cost_fi, time_fi = local_search(profits, weights, Q)
    print(f"Best Improvement - Avg Cost: {avg_cost_bi}, Time: {time_bi}")
    print(f"First Improvement - Avg Cost: {avg_cost_fi}, Time: {time_fi}")