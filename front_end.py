from collections import defaultdict
from itertools import combinations

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

def assign_ids(N, triples): #create ids for the bottom legends in output
    pegs = {}
    jumps = {}
    c = 1
    
    # Assign IDs to Jumps
    for t in range(1, N-1):
        for j in triples:
            jumps[(j[0], j[1], j[2], t)] = c
            c += 1
            
    # Assign IDs to Pegs
    for t in range(1, N):
        for h in range(1, N + 1):
            pegs[(h, t)] = c
            c += 1
    
    return pegs, jumps


def create_legend(pegs, jumps):
    legend = {}
    for key, value in pegs.items():
        legend[value] = f"Peg({key[0]},{key[1]})"
    for key, value in jumps.items():
        legend[value] = f"Jump({key[0]},{key[1]},{key[2]},{key[3]})"
    return legend


def generate_refined_clauses(N, triples, peg, jump):
    clauses = []

    for time in range(1, N):
        for A, B, C in triples:
            # Ensure valid range for jumps
            if time < N - 1:
                jump_id = jump.get((A, B, C, time))
                if jump_id:
                    # Precondition axioms for jumps
                    clauses.append(f"-{jump_id} {peg[(A, time)]}")
                    clauses.append(f"-{jump_id} {peg[(B, time)]}")
                    clauses.append(f"-{jump_id} -{peg[(C, time)]}")

                    # Causal axioms for jumps
                    # After the jump, A and B should be empty, and C should have a peg.
                    clauses.append(f"-{jump_id} -{peg[(A, time + 1)]}")
                    clauses.append(f"-{jump_id} -{peg[(B, time + 1)]}")
                    clauses.append(f"-{jump_id} {peg[(C, time + 1)]}")

    return clauses



def generate_frame_axioms(N, triples, pegs, jumps):
    frame_clauses = []

    for t in range(1, N):
        for p in range(1, N + 1):
            current_peg = pegs.get((p, t))
            next_peg = pegs.get((p, t + 1))
            possible_jumps = []
            less_jumps = []

            # identify possible jump affecting the peg's state
            for (A, B, C) in triples:
                if p == A:  # Peg jumps from A
                    jumpid = jumps.get((A, B, C, t))
                    if jumpid:
                        possible_jumps.append(jumpid)
                elif p == C:
                    jumpid = jumps.get((A, B, C, t))
                    if jumpid:
                        possible_jumps.append(jumpid)
                        less_jumps.append(jumpid) #jump for less combination

            # If the peg's state changes, generate the corresponding clause
            if current_peg and next_peg:
                frame_clauses.append(f"{current_peg} -{next_peg} " + " ".join(map(str, less_jumps)))
                frame_clauses.append(f"-{current_peg} {next_peg} " + " ".join(map(str, possible_jumps)))

    return frame_clauses


def generate_time_specific_exclusivity_clauses(jumps, include_optional_clause=True):
    jumps_by_time = defaultdict(list)
    for (A, B, C, time), jump_id in jumps.items():
        jumps_by_time[time].append(jump_id)
    
    mutual_exclusivity_clauses = []
    for time, jump_ids in jumps_by_time.items():
        for a, b in combinations(jump_ids, 2):
            mutual_exclusivity_clauses.append(f"-{a} -{b}")
        # Optional clause: At least one action per time step
        if include_optional_clause and jump_ids:
            at_least_one_clause = ' '.join(f"{jump_id}" for jump_id in jump_ids)
            mutual_exclusivity_clauses.append(at_least_one_clause)
    
    return mutual_exclusivity_clauses



def generate_starting_state_clauses(pegs, empty_hole, N):
    starting_state_clauses = []
    for hole in range(1, N + 1):
        peg_id = pegs.get((hole, 1))
        if hole == empty_hole:
            starting_state_clauses.append(f"-{peg_id}")
        else:
            starting_state_clauses.append(f"{peg_id}")
    return starting_state_clauses


def generate_ending_state_clauses(pegs, N):
    ending_state_clauses = []
    final_time = N - 1  # Assuming the final time step is N-1

    # Generate clauses for each pair of holes ensuring no two can have a peg
    for H in range(1, N + 1):
        for J in range(H + 1, N + 1):
            peg_H_id = pegs.get((H, final_time))
            peg_J_id = pegs.get((J, final_time))
            if peg_H_id and peg_J_id:  # Ensure both pegs have IDs assigned
                clause = f"-{peg_H_id} -{peg_J_id}"
                ending_state_clauses.append(clause)

    return ending_state_clauses

def read_input(file_path='front_end_input.txt'):
    with open(file_path, 'r') as file: #read input and seperate first line
        first = file.readline().strip().split()
        N, empty_hole = int(first[0]), int(first[1])
        triples = [tuple(map(int, line.strip().split())) for line in file]

    return N, empty_hole, triples

def main_refined_execution():
    N, empty_hole, triples = read_input()
    expanded_triples = triples + [(C, B, A) for A, B, C in triples]
    peg, jump = assign_ids(N, expanded_triples)
    
    clauses = generate_refined_clauses(N, expanded_triples, peg, jump)
    frame_clauses = generate_frame_axioms(N, expanded_triples, peg, jump)
    exclusive_action_clauses = generate_time_specific_exclusivity_clauses(jump)
    starting_state_clauses = generate_starting_state_clauses(peg, empty_hole, N)
    ending_state_clauses = generate_ending_state_clauses(peg, N)

    all_clauses = clauses + frame_clauses + exclusive_action_clauses + starting_state_clauses + ending_state_clauses
    
    legend = create_legend(peg, jump)
    
    with open('front_end_output.txt', 'w') as file:
        for clause in all_clauses:
            file.write(f"{clause}\n")
        
        file.write("0\n")
        for id, desc in sorted(legend.items()):
            file.write(f"{id}: {desc}\n")

main_refined_execution()


