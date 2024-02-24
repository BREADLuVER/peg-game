def read_dp_solution_and_legend(filename):
    solution = {}
    legend = {}
    start_reading_solution = False
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line == '0':
                start_reading_solution = True
                continue
            if start_reading_solution:
                if ' ' in line:
                    var, val = line.split()
                    solution[int(var)] = val == 'T'
                else:
                    var, description = line.split(maxsplit=1)
                    legend[int(var)] = description
    return solution, legend

def generate_moves_from_dp_output(filename):
    solution, legend = read_dp_solution_and_legend(filename)
    moves = [legend[var] for var, is_true in solution.items() if is_true and var in legend]
    return moves

def main():
    filename = 'dp_output.txt'
    moves = generate_moves_from_dp_output(filename)
    for move in moves:
        print(move)

if __name__ == "__main__":
    main()


