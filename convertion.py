import sys
import time

t1 = time.time()

path_to_file_to_open = sys.argv[1]
path_to_file_to_write = sys.argv[2]

with open(path_to_file_to_open, "r") as file:
    lines = file.readlines()

n, m = map(int, lines[0].split(" ")) # N = number of guests, M = number of friendship links
guests = [list(map(int, line.split(" "))) for line in lines[1:n+1]] # guests[i] = [i, c_i]
friendship_links = [[0 for _ in range(n)] for _ in range(n)] # friendship_links[i][j] = 1 if i and j are friends, 0 otherwise

for line in lines[n+1:]:
    i, j = map(int, line.split()) 
    friendship_links[i][j] = 1
    friendship_links[j][i] = 1

with open(path_to_file_to_write, "w") as lp_file:
    lp_file = open(path_to_file_to_write, "w")
    lp_file.write("Maximize\n")
    lp_file.write("z: " + " + ".join([f"{interest} x{guest_number}" for guest_number, interest in guests]) + "\n")
    lp_file.write("\nSubject To\n")

    for i in range(n):
        for j in range(i+1, n):
            if friendship_links[i][j] == 0:
                lp_file.write(f"x{i} + x{j} <= 1\n")

    lp_file.write("\nBinaries\n")
    for i in range(1, n+1):
        lp_file.write(f"x{i}\n")

    lp_file.write("End")

t2 = time.time()
print("Time to read file: ", t2-t1)
    





