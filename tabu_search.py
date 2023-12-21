# Importing necessary modules
import sys
import math
import time

# Class definition for TabuSearch algorithm
class TabuSearch:
    def __init__(self, initial_solution, guests, tabu_list_size=3):
        # Initializing the TabuSearch object with initial solution, guests, and tabu list size
        self.current_solution = initial_solution
        self.best_solution = initial_solution
        self.guests = guests
        self.tabu_list = []
        self.tabu_list_size = tabu_list_size

    def run(self, start_time, time_limit):
        # Running the TabuSearch algorithm for a specified number of iterations
        while time.time() - start_time < time_limit:
            # Generating the neighborhood solutions and their indexes
            neighbors, indexes_of_i_for_neighbors = self.get_neighborhood(self.current_solution)
            solutions = []
            
            # Calculating the interest for each neighbor solution
            for neighbor in neighbors:
                index_of_1 = [i for i, x in enumerate(neighbor) if x == 1]
                interest = sum(self.guests[i]['interest'] for i in index_of_1)
                solutions.append(interest)

            # Selecting the next solution with the maximum interest
            next_solution = neighbors[solutions.index(max(solutions))]
            next_solution_index = indexes_of_i_for_neighbors[solutions.index(max(solutions))]
            
            # Updating the best solution if the next solution is better
            if self.compare_solution(next_solution, self.best_solution):
                self.best_solution = next_solution
            
            # Updating the tabu list and current solution
            self.update_tabu_list(next_solution_index)
            self.current_solution = next_solution
        
        # Returning the best solution found
        return self.best_solution

    def get_neighborhood(self, solution, k=1):
        # Generating the neighborhood solutions by flipping each bit in the solution
        neighbors = []
        indexes_of_i_for_neighbors = []
        for i in range(len(solution)):
            # Skipping the bit if it is in the tabu list
            if i in self.tabu_list:
                continue

            neighbor = solution.copy()
            neighbor[i] = 1 if neighbor[i] == 0 else 0
            
            if self.all_guests_are_friends(neighbor):
                neighbors.append(neighbor)
                indexes_of_i_for_neighbors.append(i)

        # Returning the neighborhood solutions and their indexes
        return neighbors, indexes_of_i_for_neighbors                  

    def all_guests_are_friends(self, solution):
        indexes_of_1 = [i for i, x in enumerate(solution) if x == 1]
        for i in indexes_of_1:
            friends_of_i = self.guests[i]['friends']
            for j in indexes_of_1:
                if j != i and j not in friends_of_i:
                    return False
        return True

    def compare_solution(self, solution1, solution2):
        # Comparing two solutions based on their total interest
        indexes_of_1_for_solution1 = [i for i, x in enumerate(solution1) if x == 1]
        indexes_of_1_for_solution2 = [i for i, x in enumerate(solution2) if x == 1]
        return sum(self.guests[i]['interest'] for i in indexes_of_1_for_solution1) > sum(self.guests[i]['interest'] for i in indexes_of_1_for_solution2)
    
    def update_tabu_list(self, solution):
        # Updating the tabu list with the index of the new solution
        self.tabu_list.append(solution)
        if len(self.tabu_list) > self.tabu_list_size:
            self.tabu_list.pop(0)
    

def greedy(guests):
    # Greedy algorithm for selecting initial solution
    invited_guests = set()
    possible_guests = set(guests.keys())

    while possible_guests:
        best_guest = max(possible_guests, key=lambda i: guests[i]['interest'] * len(guests[i]['friends']))
        invited_guests.add(best_guest)
        guests[best_guest]['invited'] = True
        if not invited_guests:
            possible_guests = set(guests.keys())
        else:
            possible_guests = {i for i in guests if guests[i]['friends'].issuperset(invited_guests) and not guests[i]['invited']}

    # Returning the set of invited guests
    return invited_guests

time_limit = float(sys.argv[1])
path_to_file_to_open = sys.argv[2]

with open(path_to_file_to_open, 'r') as file:
    # Reading the number of guests and friendships
    n, m = map(int, file.readline().split())
    guests = {i: {'interest': 0, 'friends': set(), 'invited': False} for i in range(n)}

    # Reading the interests of each guest
    for _ in range(n):
        i, c_i = map(int, file.readline().split())
        guests[i]['interest'] = c_i

    # Reading the friendships between guests
    for _ in range(m):
        i, j = map(int, file.readline().split())
        guests[i]['friends'].add(j)
        guests[j]['friends'].add(i)

# Generating the initial solution using the greedy algorithm
initial_solution = greedy(guests)
boolean_vector = [1 if i in initial_solution else 0 for i in range(n)]
initial_solution = boolean_vector

# Calculating the tabu list size
# Try to make the tabu_list_size correspoding to the number of guests
tabu_list_size = math.floor((n*n) * 0.00004)

# Running the TabuSearch algorithm
tabu_search = TabuSearch(initial_solution, guests, tabu_list_size=tabu_list_size)
best_solution = tabu_search.run(start_time=time.time(), time_limit=time_limit)

# Extracting the indexes of invited guests from the best solution
invited_guests_indexes = [i for i, x in enumerate(best_solution) if x == 1]

# Calculating the total interest of invited guests
max_interest = 0
for i in invited_guests_indexes:
    max_interest += guests[i]['interest']

# Printing the results
print(f"Total score of invited guests: {max_interest}")