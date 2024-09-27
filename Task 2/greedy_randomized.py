import random
import threading

def load(filename):
    with open(filename, 'r') as f:
        n = int(f.readline().strip())
        Q = int(f.readline().strip())
        profits = list(map(int, f.readline().strip().split()))
        weights = list(map(int, f.readline().strip().split()))
    return n, Q, profits, weights

def evaluate(solution, profits, weights, capacity):
    total_profit = sum(p for p, s in zip(profits, solution) if s == 1)
    total_weight = sum(w for w, s in zip(weights, solution) if s == 1)
    if total_weight <= capacity:
        return total_profit
    else:
        # Apply a penalty proportional to the excess weight
        penalty = (total_weight - capacity) * max(profits)
        return total_profit - penalty

def constructive_heuristic(n, profits, weights, capacity, alpha, result_container):
    # Initialize empty solution
    solution = [0] * n
    remaining_capacity = capacity

    # Initialize the list of candidate items
    candidate_items = list(range(n))

    # While there are candidate items
    while candidate_items:
        # Compute the profit-to-weight ratio for candidate items
        ratios = [(profits[i] / weights[i], i) for i in candidate_items]
        # Find max and min ratios among the candidates
        max_ratio = max(ratios)[0]
        min_ratio = min(ratios)[0]
        threshold = max_ratio - alpha * (max_ratio - min_ratio)
        # Build the Restricted Candidate List (RCL)
        RCL = [item for item in ratios if item[0] >= threshold]
        # Randomly select an item from RCL
        if not RCL:
            break
        _, i = random.choice(RCL)
        # Check if item fits
        if weights[i] <= remaining_capacity:
            solution[i] = 1
            remaining_capacity -= weights[i]
        # Remove item from candidate items
        candidate_items.remove(i)

    # Store the result in the shared container
    result_container.append(solution)

def run_constructive_heuristic_with_timeout(n, profits, weights, capacity, alpha, time_limit):
    result_container = []
    thread = threading.Thread(target=constructive_heuristic, args=(n, profits, weights, capacity, alpha, result_container))
    thread.start()
    thread.join(time_limit)
    if thread.is_alive():
        # Time limit exceeded; return empty solution
        thread.join()
        return [0] * n
    else:
        return result_container[0]

def main():
    # Load data
    n, capacity, profits, weights = load('knapsack_data.txt')
    time_limit = 1  # Time limit in seconds

    best_alpha = None
    best_average_profit = float('-inf')

    alpha_values = [i / 100 for i in range(101)]  # 0.00 to 1.00
    num_runs_per_alpha = 10

    print("Tuning Alpha Values:")
    for alpha in alpha_values:
        total_profit = 0
        for _ in range(num_runs_per_alpha):
            solution = run_constructive_heuristic_with_timeout(n, profits, weights, capacity, alpha, time_limit)
            profit = evaluate(solution, profits, weights, capacity)
            total_profit += profit
        average_profit = total_profit / num_runs_per_alpha
        if average_profit > best_average_profit:
            best_average_profit = average_profit
            best_alpha = alpha
        print(f"Alpha: {alpha:.2f}, Average Profit: {average_profit}")

    print(f"\nBest alpha: {best_alpha}, with average profit: {best_average_profit}")

    # Generate 10 different initial solutions with the best alpha
    num_runs = 10000
    total_profit_best_alpha = 0
    print(f"\nConstructive Heuristic with Best Alpha ({best_alpha}):")
    for i in range(num_runs):
        solution = run_constructive_heuristic_with_timeout(n, profits, weights, capacity, best_alpha, time_limit)
        profit = evaluate(solution, profits, weights, capacity)
        total_profit_best_alpha += profit
        print(f"Run {i+1}: Profit = {profit}")
    average_profit_best_alpha = total_profit_best_alpha / num_runs
    print(f"Average Profit with Best Alpha ({best_alpha}): {average_profit_best_alpha}")

    # Purely greedy strategy (alpha=0)
    total_profit_greedy = 0
    print(f"\nPurely Greedy Strategy (Alpha=0):")
    for i in range(num_runs):
        solution = run_constructive_heuristic_with_timeout(n, profits, weights, capacity, 0, time_limit)
        profit = evaluate(solution, profits, weights, capacity)
        total_profit_greedy += profit
        print(f"Run {i+1}: Profit = {profit}")
    average_profit_greedy = total_profit_greedy / num_runs
    print(f"Average Profit with Purely Greedy Strategy: {average_profit_greedy}")

    # Purely random strategy (alpha=1)
    total_profit_random = 0
    print(f"\nPurely Random Strategy (Alpha=1):")
    for i in range(num_runs):
        solution = run_constructive_heuristic_with_timeout(n, profits, weights, capacity, 1, time_limit)
        profit = evaluate(solution, profits, weights, capacity)
        total_profit_random += profit
        print(f"Run {i+1}: Profit = {profit}")
    average_profit_random = total_profit_random / num_runs
    print(f"Average Profit with Purely Random Strategy: {average_profit_random}")

    # Compare the average profits
    print("\nComparison of Strategies:")
    print(f"Average Profit with Best Alpha ({best_alpha}): {average_profit_best_alpha}")
    print(f"Average Profit with Purely Greedy Strategy: {average_profit_greedy}")
    print(f"Average Profit with Purely Random Strategy: {average_profit_random}")

    # Determine which method is better on average
    if average_profit_best_alpha > max(average_profit_greedy, average_profit_random):
        print("The Constructive Heuristic with Best Alpha is better on average.")
    elif average_profit_greedy > max(average_profit_best_alpha, average_profit_random):
        print("The Purely Greedy Strategy is better on average.")
    else:
        print("The Purely Random Strategy is better on average.")

if __name__ == "__main__":
    main()
