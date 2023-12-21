import sys

# Getting the paths to the input and output files from command line arguments
path_to_file_to_open = sys.argv[1]
path_to_file_to_write = sys.argv[2]

# Opening the input file and reading its contents
with open(path_to_file_to_open, "r") as file:
    lines = file.readlines()

# Extracting the values of N and M from the first line of the input file
n, m = map(int, lines[0].split(" "))

# Extracting the guest information from the lines between 1 and N+1
guests = [list(map(int, line.split(" "))) for line in lines[1:n+1]]

# Creating an empty friendship_links matrix
friendship_links = [[0 for _ in range(n)] for _ in range(n)]

# Populating the friendship_links matrix based on the friendship links provided in the input file
for line in lines[n+1:]:
    i, j = map(int, line.split()) 
    friendship_links[i][j] = 1
    friendship_links[j][i] = 1

# Opening the output file for writing
with open(path_to_file_to_write, "w") as lp_file:
    lp_file = open(path_to_file_to_write, "w")
    
    # Writing the objective function to the output file
    lp_file.write("Maximize\n")
    lp_file.write("z: " + " + ".join([f"{interest} x{guest_number}" for guest_number, interest in guests]) + "\n")
    
    lp_file.write("\nSubject To\n")
    
    # Writing the friendship constraints to the output file
    for i in range(n):
        for j in range(i+1, n):
            if friendship_links[i][j] == 0:
                lp_file.write(f"x{i} + x{j} <= 1\n")
    
    lp_file.write("\nBinaries\n")
    
    # Writing the binary variable declarations to the output file
    for i in range(1, n+1):
        lp_file.write(f"x{i}\n")
    
    lp_file.write("End")
