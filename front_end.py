def read_game_board(filename):
    with open(filename, 'r') as file:
        first_line = file.readline().strip().split()
        num_holes, initial_empty = int(first_line[0]), int(first_line[1])
        triples = [tuple(map(int, line.strip().split())) for line in file]
    return num_holes, initial_empty, triples

def generate_clauses(num_holes, initial_empty, triples):
    clauses = []

    # Starting state: Specify the truth value of Peg(H,1) for each hole H.
    for hole in range(1, num_holes + 1):
        if hole == initial_empty:
            clauses.append(f"-Peg({hole},1)")
        else:
            clauses.append(f"Peg({hole},1)")
    
    # Add other clauses based on the game rules and the triples.
    # This includes precondition axioms, causal axioms, frame axioms, etc.

    return clauses

def write_clauses_to_file(clauses, filename):
    with open(filename, 'w') as file:
        for clause in clauses:
            file.write(f"{clause}\n")
        file.write("0\n")

def main(input_filename, output_filename):
    num_holes, initial_empty, triples = read_game_board(input_filename)
    clauses = generate_clauses(num_holes, initial_empty, triples)
    write_clauses_to_file(clauses, output_filename)

def generate_clauses(num_holes, initial_empty, triples):
    clauses = []
    # Example starting state clause
    clauses.append(f"-Peg({initial_empty},1)")  # Initial empty hole
    # Placeholder for generating other clauses based on triples
    for a, b, c in triples:
        # Simplified example to demonstrate adding clauses
        clauses.append(f"Jump({a},{b},{c},I) => Peg({a},I) ^ Peg({b},I) ^ ~Peg({c},I)")
    return clauses


# Example usage
input_filename = 'game_board_input.txt'
output_filename = 'clauses_output.txt'
main(input_filename, output_filename)
