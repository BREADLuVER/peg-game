def read_dp_output(dp_output_filename):
    with open(dp_output_filename, 'r') as file:
        lines = file.read().split('\n0\n')  # Split into solution and legend parts
        solution_part, legend_part = lines[0], lines[1]

        solution_lines = solution_part.strip().splitlines()
        solution = {int(var): value == 'T' for var, value in (line.split() for line in solution_lines)}

        legend_lines = legend_part.strip().splitlines()
        legend = {int(line.split()[0]): ' '.join(line.split()[1:]) for line in legend_lines}

    return solution, legend

def filter_feasible_jumps(solution, legend):
    jumps = [legend[var] for var, taken in solution.items() if taken and var in legend and 'Jump' in legend[var]]
    return jumps

def generate_moves(dp_output_filename):
    solution, legend = read_dp_output(dp_output_filename)
    if not solution:  # If there's no solution in the DP output
        return ["NO SOLUTION"]
    feasible_jumps = filter_feasible_jumps(solution, legend)
    return feasible_jumps if feasible_jumps else ["NO SOLUTION"]

def main():
    dp_output_filename = 'dp_output.txt'
    moves = generate_moves(dp_output_filename)
    if moves == ["NO SOLUTION"]:
        print("NO SOLUTION")
    else:
        print("Sequence of feasible jumps to solve the peg game:")
        for move in moves:
            print(move)

if __name__ == "__main__":
    main()




