import sys

# Getting the path to the file to open from the command-line argument
path_to_file_to_open = sys.argv[1]

# Opening the file in read mode
with open(path_to_file_to_open, 'r') as file:
    # Reading the first line of the file and extracting the values of n and m
    n, m = map(int, file.readline().split())

    # Creating a dictionary to store information about each guest
    guests = {i: {'interest': 0, 'friends': set(), 'invited': False} for i in range(n)}

    # Reading the next n lines of the file and updating the interest value for each guest
    for _ in range(n):
        i, c_i = map(int, file.readline().split())
        guests[i]['interest'] = c_i

    # Reading the next m lines of the file and updating the friends set for each guest
    for _ in range(m):
        i, j = map(int, file.readline().split())
        guests[i]['friends'].add(j)
        guests[j]['friends'].add(i)

# Creating a set to store the invited guests
invited_guests = set()

# Creating a set to store the possible guests who can be invited
possible_guests = set(guests.keys())

# Iterating until there are no more possible guests to invite
while possible_guests:
    # Finding the guest with the highest heuristic value
    # Heuristic value = interest * number of friends
    best_guest = max(possible_guests, key=lambda i: guests[i]['interest'] * len(guests[i]['friends']))

    # Adding the best guest to the invited guests set
    invited_guests.add(best_guest)

    # Marking the best guest as invited
    guests[best_guest]['invited'] = True

    # Updating the possible guests set based on the friends of the invited guests
    if not invited_guests:
        possible_guests = set(guests.keys())
    else:
        possible_guests = {i for i in guests if guests[i]['friends'].issuperset(invited_guests) and not guests[i]['invited']}

# Calculating the total score of the invited guests
max_interest_found = sum(guests[i]['interest'] for i in invited_guests)

# Printing the total score of the invited guests
print(f"Total score of invited guests: {max_interest_found}")