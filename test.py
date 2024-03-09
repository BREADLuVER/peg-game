def read_input(file_path='front_end_input.txt'):
    with open(file_path, 'r') as file:  # Read input and separate the first line
        first_line = file.readline().strip().split()
        N, empty_hole = int(first_line[0]), int(first_line[1])
        triples = [tuple(map(int, line.strip().split())) for line in file]
    return N, empty_hole, triples

def generate_ids(N, triples):
    ids = []
    id_counter = 1  # Initialize ID counter
    
    # Directly generate four jumps for each triple, without extra looping
    for A, B, C in triples:
        # Forward direction at times 1 and 2
        ids.append((id_counter, f'Jump({A},{B},{C},1)')); id_counter += 1
        ids.append((id_counter, f'Jump({A},{B},{C},2)')); id_counter += 1
        
        # Reverse direction at times 1 and 2
        ids.append((id_counter, f'Jump({C},{B},{A},1)')); id_counter += 1
        ids.append((id_counter, f'Jump({C},{B},{A},2)')); id_counter += 1
    
    # Generate Peg IDs
    for H in range(1, N+1):  # For each hole
        for I in range(1, N):  # For each time point from 1 to N-1
            ids.append((id_counter, f'Peg({H},{I})')); id_counter += 1
    
    return ids


def main_refined_execution(file_path='front_end_input.txt'):
    N, empty_hole, triples = read_input(file_path)
    # No need to expand triples with reverse directions manually; handled in generate_ids
    ids = generate_ids(N, triples)
    
    # For demonstration purposes, let's print the IDs and their corresponding atoms
    for id_pair in ids:
        print(id_pair)

# Assuming 'front_end_input.txt' contains the input data
# You can call the main function to execute the workflow
main_refined_execution('front_end_input.txt')
