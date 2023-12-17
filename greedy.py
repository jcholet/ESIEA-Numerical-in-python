import time
import sys

path_to_file_to_open = sys.argv[1]

with open(path_to_file_to_open, 'r') as file:
    n, m = map(int, file.readline().split())
    guests = {i: {'interest': 0, 'friends': set(), 'invited': False} for i in range(n)}

    for _ in range(n):
        i, c_i = map(int, file.readline().split())
        guests[i]['interest'] = c_i

    for _ in range(m):
        i, j = map(int, file.readline().split())
        guests[i]['friends'].add(j)
        guests[j]['friends'].add(i)


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

print(invited_guests)
# Verify that all invited_guests are friends
for i in invited_guests:
    for j in invited_guests:
        if i != j and j not in guests[i]['friends']:
            print("Not all invited guests are friends")
            exit(1)
max_interest_found = sum(guests[i]['interest'] for i in invited_guests)
print(f"Total score of invited guests: {max_interest_found}")