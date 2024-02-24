def read_dp_output(filename):
    solution = {}
    legend = {}
    reading_solution = True  # Start by reading the solution part
    with open(filename, 'r') as file:
        for line in file:
            if line.strip() == '0':  # Switch to reading the legend
                reading_solution = False
                continue
            if reading_solution:
                var, val = line.split()
                solution[int(var)] = val == 'T'
            else:
                var, description = line.split(maxsplit=1)
                legend[int(var)] = description
    return solution, legend

def interpret_solution(solution, legend):
    moves = []
    for var, taken in solution.items():
        if taken and var in legend and legend[var].startswith("Jump"):
            moves.append(legend[var])
    return moves

def generate_moves(dp_output_filename):
    solution, legend = read_dp_output(dp_output_filename)
    moves = interpret_solution(solution, legend)
    return moves

def main():
    dp_output_filename = 'dp_output.txt'
    moves = generate_moves(dp_output_filename)
    print("Sequence of jumps to solve the peg game:")
    for move in moves:
        print(move)

if __name__ == "__main__":
    main()



