def parse_input(dp_output_filename):
    with open(dp_output_filename, 'r') as file:
        lines = file.read().split('\n0\n')
        solution_part, legend_part = lines[0], lines[1]
        print(legend_part)
        # Parse the solution and legend parts
        solution_lines = solution_part.strip().splitlines()
        solution = {int(var): value == 'T' for var, value in (line.split() for line in solution_lines)}
        
        legend_lines = legend_part.strip().splitlines()
        legend = {int(line.split()[0]): ' '.join(line.split()[1:]) for line in legend_lines}

    return solution, legend

def jumps(solution, legend): # This function is used to filter the feasible jumps from the solution
    jumps = [legend[var] for var, taken in solution.items() if taken and var in legend]
    return jumps

def generate_moves(dp_output_filename): 
    solution, legend = parse_input(dp_output_filename)
    if not solution:
        return ["NO SOLUTION"]
    feasible_jumps = jumps(solution, legend)
    return feasible_jumps if feasible_jumps else ["NO SOLUTION"]

def write_output(output_filename, solution):
    with open(output_filename, 'w') as file:
        if solution is None:
            file.write("0\n No solution found.\n")
        else:
            for s in solution:
                file.write(f'{s} \n')

def main():
    dp_output_filename = 'dp_output.txt'
    output_filename = 'backend_output.txt'
    moves = generate_moves(dp_output_filename)
    if moves == ["NO SOLUTION"]:
        print("NO SOLUTION")
    else:
        print("Sequence of feasible jumps to solve the peg game:")
        for move in moves:
            print(move)
    write_output(output_filename, moves if moves else None)
    
if __name__ == "__main__":
    main()




