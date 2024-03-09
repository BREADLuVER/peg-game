def read_input(file_path='front_end_input.txt'):
    with open(file_path, 'r') as file:  # Read input and separate the first line
        first_line = file.readline().strip().split()
        N, empty_hole = int(first_line[0]), int(first_line[1])
        triples = [tuple(map(int, line.strip().split())) for line in file]
    return N, empty_hole, triples

class Peg:
    def __init__(self, hole, time):
        self.hole = hole
        self.time = time
        
    def __str__(self):
        return f"Peg({self.hole},{self.time})"

class Jump:
    def __init__(self, from_hole, over_hole, to_hole, time):
        self.from_hole = from_hole
        self.over_hole = over_hole
        self.to_hole = to_hole
        self.time = time
        
    def __str__(self):
        return f"Jump({self.from_hole},{self.over_hole},{self.to_hole},{self.time})"

def generate_ids(N, empty_hole, triples):
    ids = []
    all_jumps = []  # Array for all Jump objects
    all_pegs = []   # Array for all Peg objects
    id_counter = 1  # Initialize ID counter
    
    # Generate Jump objects and associate IDs
    for A, B, C in triples:
        for I in range(1, N-1):
            all_jumps.append(Jump(A, B, C, I))
            ids.append((id_counter, all_jumps[-1])); id_counter += 1
            
            all_jumps.append(Jump(C, B, A, I))
            ids.append((id_counter, all_jumps[-1])); id_counter += 1
    
    # Generate Peg objects and associate IDs after Jump IDs
    Q = len(all_jumps)  # Total number of Jump objects
    for H in range(1, N+1):
        for I in range(1, N):
            if not (H == empty_hole and I == 1):  # Skip the initial empty hole at time 1
                all_pegs.append(Peg(H, I))
                ids.append((Q + len(all_pegs), all_pegs[-1]))  # Use Q+length of all_pegs for ID association
    
    return ids, all_jumps, all_pegs


def find_id_by_attributes(jumps, pegs, obj):
    # Determine if the object is a Jump or a Peg and find its ID
    if isinstance(obj, Jump):
        for i, jump in enumerate(jumps, 1):  # Enumerate starts at 1 for ID association
            if (jump.from_hole, jump.over_hole, jump.to_hole, jump.time) == (obj.from_hole, obj.over_hole, obj.to_hole, obj.time):
                return -i  # Negated ID for jumps
    elif isinstance(obj, Peg):
        offset = len(jumps)  # Offset by the number of jumps
        for i, peg in enumerate(pegs, 1 + offset):  # Adjust enumeration for offset
            if (peg.hole, peg.time) == (obj.hole, peg.time):
                return i  # Positive ID for pegs
    return None  # Return None if not found

def generate_cnf_clauses(jumps, pegs):
    clauses = []
    for jump in jumps:
        # Find IDs for the precondition axiom components
        jump_id = find_id_by_attributes(jumps, pegs, jump)
        peg_at_start_id = find_id_by_attributes(jumps, pegs, Peg(jump.from_hole, jump.time))
        peg_over_id = find_id_by_attributes(jumps, pegs, Peg(jump.over_hole, jump.time))
        peg_at_end_id = find_id_by_attributes(jumps, pegs, Peg(jump.to_hole, jump.time))
        
        # Create CNF clauses for the precondition axioms
        clauses.append(f"{jump_id} {peg_at_start_id}")
        clauses.append(f"{jump_id} {peg_over_id}")
        clauses.append(f"{jump_id} {-(peg_at_end_id)}")
    return clauses

def main_refined_execution(file_path='front_end_input.txt'):
    N, empty_hole, triples = read_input(file_path)
    
    # Assuming generate_ids now correctly adds descriptive strings
    ids, all_jumps, all_pegs = generate_ids(N, empty_hole, triples)
    
    cnf_clauses = generate_cnf_clauses(all_jumps, all_pegs)

    # Print CNF clauses
    for clause in cnf_clauses:
        print(clause)

    # Print IDs with their descriptive strings
    for id_number, description in ids:
        print(f"{id_number}: {description}")

main_refined_execution('front_end_input.txt')