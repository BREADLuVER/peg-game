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


def generate_time_specific_exclusivity_clauses(jump_ids):
    # Organize jumps by time step
    jumps_by_time = {}
    for (A, B, C, time), jump_id in jump_ids.items():
        if time not in jumps_by_time:
            jumps_by_time[time] = []
        jumps_by_time[time].append(jump_id)
    
    # Generate exclusivity clauses within each time step
    mutual_exclusivity_clauses = []
    for time, jumps in jumps_by_time.items():
        for i in range(len(jumps)):
            for j in range(i + 1, len(jumps)):
                clause = f"-{jumps[i]} -{jumps[j]}"
                mutual_exclusivity_clauses.append(clause)
    
    return mutual_exclusivity_clauses


def generate_starting_state_clauses(peg_ids, empty_hole, N):
    starting_state_clauses = []
    for hole in range(1, N + 1):
        peg_id = peg_ids.get((hole, 1))
        if hole == empty_hole:
            starting_state_clauses.append(f"-{peg_id}")
        else:
            starting_state_clauses.append(f"{peg_id}")
    return starting_state_clauses


def create_legend(peg_ids, jump_ids):
    legend = {}
    for key, value in peg_ids.items():
        legend[value] = f"Peg({key[0]},{key[1]})"
    for key, value in jump_ids.items():
        legend[value] = f"Jump({key[0]},{key[1]},{key[2]},{key[3]})"
    return legend


def generate_ending_state_clauses(peg_ids, N):
    ending_state_clauses = []
    final_time = N - 1  # Assuming the final time step is N-1

    # Generate clauses for each pair of holes ensuring no two can have a peg
    for H in range(1, N + 1):
        for J in range(H + 1, N + 1):  # Start J from H+1 to avoid duplicate pairs and self-comparison
            peg_H_id = peg_ids.get((H, final_time))
            peg_J_id = peg_ids.get((J, final_time))
            if peg_H_id and peg_J_id:  # Ensure both pegs have IDs assigned
                clause = f"-{peg_H_id} -{peg_J_id}"
                ending_state_clauses.append(clause)

    return ending_state_clauses

def read_input(file_path='front_end_input.txt'):
    with open(file_path, 'r') as file:
        first_line = file.readline().strip().split()
        N, empty_hole = int(first_line[0]), int(first_line[1])
        triples = [tuple(map(int, line.strip().split())) for line in file]

    return N, empty_hole, triples

def main_refined_execution():
    N, empty_hole, triples = read_input()
    # expanded triples to include both directions of jumps
    expanded_triples = triples + [(C, B, A) for A, B, C in triples]

    peg_ids, jump_ids = assign_ids(N, expanded_triples)
    
    # Generate refined clauses for direct implications
    clauses = generate_refined_clauses(N, expanded_triples, peg_ids, jump_ids)
    
    # Generate frame axioms considering the changes in peg states and possible jumps
    frame_clauses = generate_frame_axioms(N, expanded_triples, peg_ids, jump_ids)

    exclusive_action_clauses = generate_time_specific_exclusivity_clauses(jump_ids)
    
    starting_state_clauses = generate_starting_state_clauses(peg_ids, empty_hole, N)
    
    # Combine all clauses, now including the starting state
    ending_state_clauses = generate_ending_state_clauses(peg_ids, N)

    # Combine all clauses, now including the ending state
    all_clauses = clauses + frame_clauses + exclusive_action_clauses + starting_state_clauses + ending_state_clauses
    
    # Generate the legend for ID to description mapping
    legend = create_legend(peg_ids, jump_ids)
    
    with open('output.txt', 'w') as file:
        for clause in all_clauses:
            file.write(f"{clause}\n")
        
        file.write("\nLegend:\n")
        for id, desc in sorted(legend.items()):
            file.write(f"{id}: {desc}\n")

main_refined_execution()


