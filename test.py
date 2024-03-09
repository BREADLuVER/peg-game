def read_input(file_path='front_end_input.txt'):
    with open(file_path, 'r') as file:  # Read input and separate the first line
        first_line = file.readline().strip().split()
        N, empty_hole = int(first_line[0]), int(first_line[1])
        triples = [tuple(map(int, line.strip().split())) for line in file]
    return N, empty_hole, triples

def generate_ids(N, empty_hole, triples):
    ids = []
    id_counter = 1  # Initialize ID counter
    
    # Adjust Jump ID generation to align with the specified pattern
    for A, B, C in triples:
        for I in range(1, N-1, 2):  # Cover all valid time points, assuming two jumps per triple per time
            # Ensure to not exceed N-2
            if I < N - 1:
                ids.append((id_counter, f'Jump({A},{B},{C},{I})')); id_counter += 1
                ids.append((id_counter, f'Jump({A},{B},{C},{I+1})')); id_counter += 1
                
                ids.append((id_counter, f'Jump({C},{B},{A},{I})')); id_counter += 1
                ids.append((id_counter, f'Jump({C},{B},{A},{I+1})')); id_counter += 1
    
    # Generate Peg IDs after all Jump IDs, considering the initial empty hole
    for H in range(1, N+1):  # For each hole
        for I in range(1, N):  # For each time point from 1 to N-1
            if not (H == empty_hole and I == 1):  # Skip the initial empty hole at time 1
                ids.append((id_counter, f'Peg({H},{I})')); id_counter += 1
    
    return ids


def main_refined_execution(file_path='front_end_input.txt'):
    N, empty_hole, triples = read_input(file_path)
    ids = generate_ids(N, empty_hole,  triples)
 
    for id_number in ids:
        print(id_number)
main_refined_execution('front_end_input.txt')
