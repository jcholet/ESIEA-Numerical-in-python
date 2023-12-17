import sys
import time
import random

class Ant:
    def __init__(self, guests, alpha=1, beta=1):
        self.guests = guests
        self.alpha = alpha
        self.beta = beta

    def build_solution(self):
        selected_guests = set()
        remaining_guests = set(self.guests.keys())

        while remaining_guests:
            probabilities = {}
            total_probability = 0
            for guest in remaining_guests:
                if can_be_invited(guests, selected_guests, guest):
                    probability = (guests[guest]['pheromone'] ** self.alpha) * (guests[guest]['heuristic'] ** self.beta)
                    probabilities[guest] = probability
                    total_probability += probability
            
            normalized_probabilities = {guest: probability / total_probability for guest, probability in probabilities.items()}
            if not normalized_probabilities:
                break
            selected_guest = random.choices(list(normalized_probabilities.keys()), weights=normalized_probabilities.values())[0]
            selected_guests.add(selected_guest)
            remaining_guests.remove(selected_guest)
        
        return selected_guests

def can_be_invited(guests, selected_guests, guest):
    if not selected_guests:
        return True
    else:
        return guests[guest]['friends'].issuperset(selected_guests) and not guests[guest]['invited']


def running_aco(n, guests, start_time, time_limit, evaporation_rate=0.95, alpha=2, beta=1, coefficient=1.05):
    best_solution = None
    best_interest = float('-inf')

    while time.time() - start_time < time_limit:
        ants = [Ant(guests, alpha, beta) for _ in range(10)]

        for ant in ants:
            solution = ant.build_solution()
            interest = sum(guests[i]['interest'] for i in solution)
            if interest > best_interest:
                best_solution = solution
                best_interest = interest
        
        max_pheromone = max(guests[i]['pheromone'] for i in range(n))
        total_pheromone = sum(guests[i]['pheromone'] for i in range(n))

        for guest in guests:
            guests[guest]['pheromone'] *= evaporation_rate
            if guest in best_solution:
                guests[guest]['pheromone'] += coefficient * (max_pheromone - guests[guest]['pheromone']) / total_pheromone

    return best_solution, best_interest

time_limit = float(sys.argv[1]) - 5
path_to_file_to_open = sys.argv[2]

with open(path_to_file_to_open, 'r') as file:
    n, m = map(int, file.readline().split())
    guests = {i: {'interest': 0, 'friends': set(),'invited': False, 'heuristic': 0, 'pheromone': 0} for i in range(n)}

    for _ in range(n):
        i, c_i = map(int, file.readline().split())
        guests[i]['interest'] = c_i

    for _ in range(m):
        i, j = map(int, file.readline().split())
        guests[i]['friends'].add(j)
        guests[j]['friends'].add(i)

    # Calculate heuristic for each guest
    for i in guests:
        guests[i]['heuristic'] = guests[i]['interest'] * len(guests[i]['friends'])

# Initialize pheromone for each guest
for i in guests:
    guests[i]['pheromone'] = guests[i]['heuristic'] / sum(guests[i]['heuristic'] for i in guests)

best_solution, best_score = running_aco(n, guests, time.time(), time_limit)
print(f"Best solution found: {best_solution}")
print(f"Best interest found: {best_score}")