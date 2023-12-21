import sys
import time
import random

# Definition of the Ant class
class Ant:
    def __init__(self, guests, alpha=1, beta=1):
        self.guests = guests
        self.alpha = alpha
        self.beta = beta

    def build_solution(self):
        # Set to store selected guests
        selected_guests = set()
        # Set to store remaining guests
        remaining_guests = set(self.guests.keys())

        # Constructing the solution
        while remaining_guests:
            # Dictionary to store probabilities
            probabilities = {}
            # Total probability
            total_probability = 0

            # Calculating probabilities for each remaining guest
            for guest in remaining_guests:
                if can_be_invited(guests, selected_guests, guest):
                    probability = (guests[guest]['pheromone'] ** self.alpha) * (guests[guest]['heuristic'] ** self.beta)
                    probabilities[guest] = probability
                    total_probability += probability
            
            # Normalizing probabilities
            normalized_probabilities = {guest: probability / total_probability for guest, probability in probabilities.items()}
            
            # Break if no normalized probabilities exist
            if not normalized_probabilities:
                break
            
            # Selecting a guest based on normalized probabilities
            selected_guest = random.choices(list(normalized_probabilities.keys()), weights=normalized_probabilities.values())[0]
            selected_guests.add(selected_guest)
            remaining_guests.remove(selected_guest)
        
        return selected_guests

# Function to check if a guest can be invited
def can_be_invited(guests, selected_guests, guest):
    if not selected_guests:
        return True
    else:
        return guests[guest]['friends'].issuperset(selected_guests) and not guests[guest]['invited']

# Function to run the Ant Colony Optimization algorithm
def running_aco(n, guests, start_time, time_limit, evaporation_rate=0.95, alpha=2, beta=1, coefficient=1.05):
    best_solution = None
    best_interest = float('-inf')

    # Running the algorithm until time limit is reached
    while time.time() - start_time < time_limit:
        ants = [Ant(guests, alpha, beta) for _ in range(10)]

        # Constructing solutions for each ant
        for ant in ants:
            solution = ant.build_solution()
            
            # Calculating interest for the solution
            interest = sum(guests[i]['interest'] for i in solution)
            
            # Updating best solution and interest if necessary
            if interest > best_interest:
                best_solution = solution
                best_interest = interest
        
        # Calculating maximum and total pheromone levels
        max_pheromone = max(guests[i]['pheromone'] for i in range(n))
        total_pheromone = sum(guests[i]['pheromone'] for i in range(n))

        # Updating pheromone levels
        for guest in guests:
            guests[guest]['pheromone'] *= evaporation_rate
            if guest in best_solution:
                guests[guest]['pheromone'] += coefficient * (max_pheromone - guests[guest]['pheromone']) / total_pheromone

    return best_solution, best_interest

# Reading command line arguments : argv[1] = time limit, argv[2] = path to input file
time_limit = float(sys.argv[1]) - 5
path_to_file_to_open = sys.argv[2]

# Opening and reading the input file
with open(path_to_file_to_open, 'r') as file:
    # Reading the first line of the file and extracting the values of n and m
    n, m = map(int, file.readline().split())

    # Creating a dictionary to store information about each guest
    guests = {i: {'interest': 0, 'friends': set(),'invited': False, 'heuristic': 0, 'pheromone': 0} for i in range(n)}

    # Reading guest interests
    for _ in range(n):
        i, c_i = map(int, file.readline().split())
        guests[i]['interest'] = c_i

    # Reading guest friendships
    for _ in range(m):
        i, j = map(int, file.readline().split())
        guests[i]['friends'].add(j)
        guests[j]['friends'].add(i)

    # Calculating heuristic for each guest
    for i in guests:
        guests[i]['heuristic'] = guests[i]['interest'] * len(guests[i]['friends'])

# Initializing pheromone for each guest
for i in guests:
    guests[i]['pheromone'] = guests[i]['heuristic'] / sum(guests[i]['heuristic'] for i in guests)

# Running the Ant Colony Optimization algorithm
best_solution, best_score = running_aco(n, guests, time.time(), time_limit)

# Printing the best solution and interest found
print(f"Best interest found: {best_score}")