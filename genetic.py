import random
import time
import copy
import sys

# Function to read input from a file
def read_input(filename):
    with open(filename, 'r') as file:
        data = file.readlines()
        N, M = map(int, data[0].split())
        interests = {i: {'interest': 0, 'invited': False, 'errors': 0} for i in range(N)}
        friendships = {i: {'friends': set()} for i in range(N)}

        # Read interests of each person
        for i in range(1, N + 1):
            person, interest = map(int, data[i].split())
            interests[person]['interest'] = interest

        # Read friendships between people
        for i in range(N + 1, N + M + 1):
            person1, person2 = map(int, data[i].split())
            friendships[person1]['friends'].add(person2)
            friendships[person2]['friends'].add(person1)
    
    return N, interests, friendships

# Greedy solution algorithm
def greedy_solution(interests, friendships):
    interests = copy.deepcopy(interests)
    invited_guests = set()
    possible_guests = set(interests.keys())
    
    while possible_guests:
        # Select the guest with the highest interest multiplied by the number of friends
        best_guest = max(possible_guests, key=lambda i: interests[i]['interest'] * len(friendships[i]['friends']))
        invited_guests.add(best_guest)
        interests[best_guest]['invited'] = True

        # Update the set of possible guests based on the friendships and invitations
        if not invited_guests:
            possible_guests = set(interests.keys())
        else:
            possible_guests = {i for i in friendships if friendships[i]['friends'].issuperset(invited_guests) and not interests[i]['invited']}
    
    return interests

# Greedy algorithm for repairing a solution

# Function to repair a solution using a greedy approach
def greedy_for_repairing(child, friendships, invited):
    child = copy.deepcopy(child)
    invited_guests = set()

    # Add the initially invited guests to the set
    invited_guests.update(invited)

    # Get the friendships of the invited guests
    friendships_of_invited = [friendships[i]['friends'] for i in invited_guests]

    # If there are no friendships among the invited guests, return the child as it is
    if len(friendships_of_invited) == 0:
        return child
    
    # Find the common friends among the invited guests
    intersected_friends = set.intersection(*friendships_of_invited)

    # Continue adding guests until there are no more common friends
    while intersected_friends:
        # Select the guest with the highest interest multiplied by the number of friends
        best_guest = max(intersected_friends, key=lambda i: child[i]['interest'] * len(friendships[i]['friends']))
        invited_guests.add(best_guest)
        child[best_guest]['invited'] = True

        # Update the friendships of the invited guests
        friendships_of_invited = [friendships[i]['friends'] for i in invited_guests]
        intersected_friends = set.intersection(*friendships_of_invited)

    return child


# Randomized greedy solution algorithm
def randomized_greedy(interests, friendships):
    interests = copy.deepcopy(interests)
    invited_guests = set()
    possible_guests = set(interests.keys())
    
    while possible_guests:
        # Assign weights to each guest based on their interest multiplied by the number of friends
        weighted_guests = [(index, interests[index]['interest'] * len(friendships[index]['friends'])) for index in possible_guests]
        # Randomly select a guest based on the weights
        randomized_guest = random.choices([guest for guest, _ in weighted_guests], weights=[weight for _, weight in weighted_guests])[0]
        invited_guests.add(randomized_guest)
        interests[randomized_guest]['invited'] = True

        # Update the set of possible guests based on the friendships and invitations
        if not invited_guests:
            possible_guests = set(interests.keys())
        else:
            possible_guests = {i for i in friendships if friendships[i]['friends'].issuperset(invited_guests) and not interests[i]['invited']}
    
    return interests

# Generate the initial population of solutions
def initial_population(size, interests, friendships):
    population = []
    initial_solution = greedy_solution(interests, friendships)
    population.append(initial_solution)
    
    for _ in range(1, size):
        random_solution = randomized_greedy(interests, friendships)
        population.append(random_solution)
    
    return population

# Evaluate the fitness of an individual solution
def evaluate(individual):
    return sum([individual[i]['interest'] for i in individual if individual[i]['invited']])

# Perform selection and reproduction to create the next generation
def selection_reproduction(population, T_prime):
    selected = []

    total_interest = 0
    for i in range(len(population)):
        individual = population[i]
        total_interest += sum(individual[person]['interest'] for person in individual if individual[person]['invited'])
    
    # Calculate the probabilities for each individual
    probabilities = []
    for i in range(len(population)):
        individual = population[i]
        probabilities.append(sum(individual[person]['interest'] for person in individual if individual[person]['invited']) / total_interest)

    # Randomly select individuals based on their probabilities
    for i in range(T_prime):
        selected.append(random.choices(population, weights=probabilities)[0])
    
    return selected

# Perform crossover between two parents to create two children
def crossover(crossover_prob, parent_1, parent_2):
    if random.random() < crossover_prob:
        crossover_point = random.randint(1, min(len(parent_1), len(parent_2)) - 1)

        child_1 = {key: parent_1[key] for key in list(parent_1)[:crossover_point]}
        child_1.update({key: parent_2[key] for key in list(parent_2)[crossover_point:]})
        
        child_2 = {key: parent_2[key] for key in list(parent_2)[:crossover_point]}
        child_2.update({key: parent_1[key] for key in list(parent_1)[crossover_point:]})
    
    else:
        child_1 = parent_1
        child_2 = parent_2
    
    return child_1, child_2

# Perform mutation on a child solution
def mutation(child):
    for i in range(len(child)):
        if random.random() < 2/len(child):
            if child[i]['invited']:
                child[i]['invited'] = False
            else:
                child[i]['invited'] = True
    
    return child

# Repair a solution by removing guests with friendship conflicts
def repair(friendships, child):
    invited_index = [i for i in range(len(child)) if child[i]['invited'] == True]

    for guest_index in invited_index:
        for other_guest_index in invited_index:
            if guest_index != other_guest_index and other_guest_index not in friendships[guest_index]['friends']:
                child[guest_index]['errors'] += 1

    while(sum([child[i]['errors'] for i in invited_index]) > 0):
        guest_to_remove = random.choices(invited_index, weights=[child[i]['errors'] for i in invited_index])[0]
        
        child[guest_to_remove]['invited'] = False
        child[guest_to_remove]['errors'] = 0
        invited_index.remove(guest_to_remove)
        
        for guest_index in invited_index:
            child[guest_index]['errors'] = 0
        
        for guest_index in invited_index:
            for other_guest_index in invited_index:
                if guest_index != other_guest_index and other_guest_index not in friendships[guest_index]['friends']:
                    child[guest_index]['errors'] += 1

    child = greedy_for_repairing(child, friendships, invited_index)

    return child

# Perform selection and survival to determine the next generation
def selection_survival(population, T):
    sorted_population = sorted(enumerate(population), key=lambda x: evaluate(x[1]), reverse=True)

    return [elem[1] for elem in sorted_population[:T]]

# Convert the population from a list to a dictionary
def list_to_dict(population_list):
    population_dict = {}

    for idx, individual in enumerate(population_list):
        population_dict[idx] = individual
    
    return population_dict

# Function to run the genetic algorithm
def genetic_algorithm(filename, duration=40, T=400, T_prime=100, crossover_prob=0.8):
    start_time = time.time()
    N, interests, friendships = read_input(filename)
    population = initial_population(T, interests, friendships)
    f_best = max([evaluate(individual) for individual in population])
    
    elapsed_time = 0
    # The algorithm runs until the elapsed time exceeds the specified duration.
    while elapsed_time < duration:
        M = selection_reproduction(population, T_prime)
        population_T = copy.deepcopy(M)
        population_T_prime = []

        # The algorithm performs crossover and mutation on pairs of parents to create two children.
        while len(population_T) >= 2:
            parent_1, parent_2 = {}, {}
            
            parent_1 = random.choice(population_T)
            population_T.remove(parent_1)

            parent_2 = random.choice(population_T)
            population_T.remove(parent_2)

            child_1 = {}
            child_2 = {}

            child_1, child_2 = crossover(crossover_prob, parent_1, parent_2)
            child_1 = mutation(child_1)
            child_2 = mutation(child_2)

            child_1 = repair(friendships, child_1)
            child_2 = repair(friendships, child_2)

            population_T_prime.append(child_1)
            population_T_prime.append(child_2)
        
        # The algorithm updates the population by adding the new children.
        population = population + population_T_prime
        population = population + M
        f_best_prime = max([evaluate(individual) for individual in population])
        if f_best < f_best_prime:
            f_best = f_best_prime
        population = selection_survival(population, T)
        elapsed_time = time.time() - start_time
    
    return f_best

# Get the path to the file to open, time limit from command line arguments
time_limit = int(sys.argv[1])
path_to_file_to_open = sys.argv[2]

# Run the genetic algorithm and get the best solution and interest
best_interest = genetic_algorithm(path_to_file_to_open, duration=time_limit)

# Print the best interest found
print(f"Best interest found: {best_interest}")