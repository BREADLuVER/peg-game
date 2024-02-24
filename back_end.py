def read_dp_output(filename):
    solution = {}
    legend = {}
    reading_solution = True
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line == '0':
                reading_solution = False
                continue
            if reading_solution:
                var, val = line.split()
                solution[int(var)] = val == 'T'
            else:
                var, description = line.strip().split(maxsplit=1)
                legend[int(var)] = description
    return solution, legend

def filter_feasible_jumps(solution, legend):
    jumps = []
    for var, taken in solution.items():
        if taken and var in legend and legend[var].startswith("Jump"):
            jump_details = legend[var]
            # Additional logic to filter out infeasible jumps could be implemented here
            jumps.append(jump_details)
    return jumps

def generate_moves(dp_output_filename):
    solution, legend = read_dp_output(dp_output_filename)
    feasible_jumps = filter_feasible_jumps(solution, legend)
    return feasible_jumps

def main():
    dp_output_filename = 'dp_output.txt'
    moves = generate_moves(dp_output_filename)
    print("Sequence of feasible jumps to solve the peg game:")
    for move in moves:
        print(move)

if __name__ == "__main__":
    main()



