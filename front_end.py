class Peg:
    def __init__(self, hole, time):
        self.hole = hole
        self.time = time

class Jump:
    def __init__(self, start, over, end, time):
        self.start = start
        self.over = over
        self.end = end
        self.time = time

def assign_ids(N, triples):
    peg_ids = {}
    jump_ids = {}
    counter = 1
    
    # Assign IDs to Pegs
    for time in range(1, N):
        for hole in range(1, N + 1):
            peg_ids[(hole, time)] = counter
            counter += 1
    
    # Assign IDs to Jumps
    for time in range(1, N-1):
        for triple in triples:
            jump_ids[(triple[0], triple[1], triple[2], time)] = counter
            counter += 1
    
    return peg_ids, jump_ids

def generate_refined_clauses(N, triples, peg_ids, jump_ids):
    clauses = []

    for time in range(1, N):
        for A, B, C in triples:
            # Ensure we're within the valid range for jumps
            if time < N - 1:
                jump_id = jump_ids.get((A, B, C, time))
                if jump_id:
                    # Precondition axioms for jumps
                    clauses.append(f"-{jump_id} {peg_ids[(A, time)]}")
                    clauses.append(f"-{jump_id} {peg_ids[(B, time)]}")
                    clauses.append(f"-{jump_id} -{peg_ids[(C, time)]}")

                    clauses.append(f"-{jump_id} -{peg_ids[(A, time + 1)]}")
                    clauses.append(f"-{jump_id} -{peg_ids[(B, time + 1)]}")
                    clauses.append(f"-{jump_id} {peg_ids[(C, time + 1)]}")
                    
    return clauses


def generate_frame_axioms(N, triples, peg_ids, jump_ids):
    frame_clauses = []

    for time in range(1, N):
        for peg in range(1, N + 1):
            current_peg = peg_ids.get((peg, time))
            next_peg = peg_ids.get((peg, time + 1))
            possible_jumps = []
            short_jumps = []

            # Identify possible jumps affecting the peg's state
            for (A, B, C) in triples:
                if peg == A:  # Peg jumps from A
                    jump_id = jump_ids.get((A, B, C, time))
                    if jump_id:
                        possible_jumps.append(jump_id)
                elif peg == C:  # Peg lands in C
                    jump_id = jump_ids.get((A, B, C, time))
                    if jump_id:
                        possible_jumps.append(jump_id)
                        short_jumps.append(jump_id)
                # Add conditions for peg being jumped over, B, if necessary

            # If the peg's state changes, generate the corresponding clause
            if current_peg and next_peg:  # Check if IDs exist for both times
                # Generate clause for peg disappearing
                frame_clauses.append(f"{current_peg} -{next_peg} " + " ".join(map(str, short_jumps)))
                # Generate clause for peg appearing
                frame_clauses.append(f"-{current_peg} {next_peg} " + " ".join(map(str, possible_jumps)))

    return frame_clauses


def create_legend(peg_ids, jump_ids):
    legend = {}
    for key, value in peg_ids.items():
        legend[value] = f"Peg({key[0]},{key[1]})"
    for key, value in jump_ids.items():
        legend[value] = f"Jump({key[0]},{key[1]},{key[2]},{key[3]})"
    return legend

# Make sure to define all necessary functions and classes as per the previous discussions
# Ensure you have the correct logic for assigning IDs and generating clauses

# Implement the main function with the refined logic
def main_refined_execution():
    N = 4  # Example configuration
    # Expanded triples to include both directions of jumps
    expanded_triples = [(1, 2, 3), (2, 3, 4), (3, 4, 1), (4, 1, 2)] + [(C, B, A) for A, B, C in [(1, 2, 3), (2, 3, 4), (3, 4, 1), (4, 1, 2)]]
    
    # Assign IDs to pegs and jumps
    peg_ids, jump_ids = assign_ids(N, expanded_triples)
    
    # Generate refined clauses for direct implications
    clauses = generate_refined_clauses(N, expanded_triples, peg_ids, jump_ids)
    
    # Generate frame axioms considering the changes in peg states and possible jumps
    frame_clauses = generate_frame_axioms(N, expanded_triples, peg_ids, jump_ids)
    
    # Combine all clauses
    all_clauses = clauses + frame_clauses
    
    # Generate the legend for ID to description mapping
    legend = create_legend(peg_ids, jump_ids)
    
    # Print all clauses for verification
    for clause in all_clauses:
        print(clause)
    
    # Print the legend
    print("\nLegend:")
    for id, desc in sorted(legend.items()):
        print(f"{id}: {desc}")

main_refined_execution()


