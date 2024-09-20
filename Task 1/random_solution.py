import random
import threading
import time

def load(filename):
    with open(filename, 'r') as f:
        n = int(f.readline().strip())
        Q = int(f.readline().strip())
        profits = list(map(int, f.readline().strip().split()))
        weights = list(map(int, f.readline().strip().split()))
    
    return n, Q, profits, weights

def random_solution(n, result, stop_event):
    solution = [random.choice([0, 1]) for _ in range(n)]
    # Simular um tempo de execução longo para teste
    for _ in range(10):
        if stop_event.is_set():
            return
        time.sleep(0.1)
    result.append(solution)

n, Q, profits, weights = load('knapsack_data.txt')
time_limit = 0.1
result = []
stop_event = threading.Event()

# Criar e iniciar a thread
thread = threading.Thread(target=random_solution, args=(n, result, stop_event))
thread.start()

# Esperar a thread terminar com um limite de tempo
thread.join(time_limit)

# Verificar se a thread ainda está ativa
if thread.is_alive():
    stop_event.set()  # Sinalizar para a thread terminar
    thread.join()  # Esperar a thread terminar
    random_sol = [0] * n  # Solução vazia
else:
    random_sol = result[0]

print(f"Random solution: {random_sol}")