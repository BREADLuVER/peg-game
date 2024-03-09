def read_input(file_path='front_end_input.txt'):
    with open(file_path, 'r') as file:  # Read input and separate the first line
        first_line = file.readline().strip().split()
        N, empty_hole = int(first_line[0]), int(first_line[1])
        triples = [tuple(map(int, line.strip().split())) for line in file]
    return N, empty_hole, triples

def generate_ids(N, triples):
    id_list = []
    id_counter = 1  # Initialize ID counter

    # Generating IDs for Jumps
    for A, B, C in triples:
        for i in [1, 2]:  # Assuming time points per the example given
            id_list.append((id_counter, f'Jump({A},{B},{C},{i})')); id_counter += 1
            id_list.append((id_counter, f'Jump({C},{B},{A},{i})')); id_counter += 1
            
    # Generating IDs for Pegs
    for H in range(1, N+1):
        for I in range(1, N):
            id_list.append((id_counter, f'Peg({H},{I})')); id_counter += 1

    return id_list


def encode_preconditions(id_list, triples, N):
    # Create a lookup dictionary from the ID list
    ids = {atom: id_number for id_number, atom in id_list}
    
    clauses = []
    for A, B, C in triples:
        for i in range(1, N-1):  # Time I for jumps
            jump_id = ids[f'Jump({A},{B},{C},{i})']
            # Precondition 1: A must have a peg
            clauses.append((-jump_id, ids[f'Peg({A},{i})']))
            # Precondition 2: B must have a peg
            clauses.append((-jump_id, ids[f'Peg({B},{i})']))
            # Precondition 3: C must not have a peg at I
            clauses.append((-jump_id, -ids[f'Peg({C},{i})']))
    return clauses


def main_refined_execution(file_path='front_end_input.txt'):
    N, empty_hole, triples = read_input(file_path)
    id_list = generate_ids(N, triples)
    
    clauses = encode_preconditions(id_list, triples, N)
    
    # Print CNF clauses for the preconditions
    print("\nEncoded Preconditions (CNF Clauses):")
    for clause in clauses:
        # Joining IDs with a space, handling negative signs for negation
        print(' '.join(str(id) for id in clause))

        # Print each ID and its corresponding atom
    print("ID and Atom List:")
    for id_number, atom in id_list:
        print(f'{id_number} {atom}')
main_refined_execution('front_end_input.txt')
