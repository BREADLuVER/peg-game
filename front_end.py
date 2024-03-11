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


def precondition_axioms(N, triples, peg, jump):
    '''generate the precondition clauses for the peg solitaire problem'''
    clauses = []
    for time in range(1, N): # Iterate over each time step
        for A, B, C in triples:
            if time < N - 1:
                jump_id = jump.get((A, B, C, time))  # Get the ID for this specific jump
                if jump_id:
                    # Generate the precondition axioms in CNF
                    clauses.append(f"-{jump_id} {peg[(A, time)]}")
                    clauses.append(f"-{jump_id} {peg[(B, time)]}")
                    clauses.append(f"-{jump_id} -{peg[(C, time)]}")

    return clauses


def causal_axioms(N, triples, peg, jump):
    '''generate the causal clauses for the peg solitaire problem'''
    causal_clauses = []

    for time in range(1, N - 1):  # Iterate over each time step, except the last one since it cannot lead to a next state
        for A, B, C in triples:
            jump_id = jump.get((A, B, C, time))
            if jump_id:
                # Create the causal effect clauses
                causal_clauses.append(f"-{jump_id} -{peg[(A, time + 1)]}")
                causal_clauses.append(f"-{jump_id} -{peg[(B, time + 1)]}")
                causal_clauses.append(f"-{jump_id} {peg[(C, time + 1)]}")
    return causal_clauses

def frame_axioms(N, triples, pegs, jumps):
    '''generate the frame clauses for the peg solitaire problem'''
    frame_clauses = []

    # generate clauses for disappearance of pegs
    for t in range(1, N):
        for h in range(1, N + 1):
            current_peg = pegs.get((h, t))
            next_peg = pegs.get((h, t + 1))
            
            if current_peg and next_peg:
                disappearance_transitions = []
                # check for jumps starting from h or jumping over h for disappearance
                for A, B, C in triples:
                    if A == h or B == h:  # Jumps from or over h lead to disappearance
                        jump_id = jumps.get((A, B, C, t))
                        if jump_id:
                            disappearance_transitions.append(str(jump_id))

                if disappearance_transitions:
                    frame_clause_disappearance = f"-{current_peg} {next_peg} " + " ".join(disappearance_transitions)
                    frame_clauses.append(frame_clause_disappearance)
    
    # generate clauses for appearance of pegs
    for t in range(1, N):
        for h in range(1, N + 1):
            current_peg = pegs.get((h, t))
            next_peg = pegs.get((h, t + 1))
            # if there are transitions that cause the peg to appear, add a clause
            if current_peg and next_peg:
                appearance_transitions = []
                # check for jumps ending at h for appearance
                for A, B, C in triples:
                    if C == h:  # Jumps ending at h
                        jump_id = jumps.get((A, B, C, t))
                        if jump_id:
                            appearance_transitions.append(str(jump_id))

                # If there are transitions that cause the peg to appear, add a clause
                if appearance_transitions:
                    frame_clause_appearance = f"{current_peg} -{next_peg} " + " ".join(appearance_transitions)
                    frame_clauses.append(frame_clause_appearance)

    return frame_clauses


def time_clauses(N, jumps, optional_at_least_one=True):
    '''generate the time clauses for the peg solitaire problem'''
    mutual_exclusivity_clauses = []
    at_least_one_action_clauses = []

    # Group jumps by their time step
    jumps_by_time = {}
    for (A, B, C, time), jump_id in jumps.items():
        if time not in jumps_by_time:
            jumps_by_time[time] = []
        jumps_by_time[time].append(jump_id)

    # Generate mutual exclusivity clauses for each time step
    for time, jump_ids in jumps_by_time.items():
        # Mutual exclusivity: No two jumps can occur at the same time
        for i in range(len(jump_ids)):
            for j in range(i + 1, len(jump_ids)):
                mutual_exclusivity_clauses.append(f"-{jump_ids[i]} -{jump_ids[j]}")
        if optional_at_least_one and jump_ids:
            at_least_one_action_clauses.append(" ".join([str(jump_id) for jump_id in jump_ids]))

    all_clauses = mutual_exclusivity_clauses + ([" ".join(at_least_one_action_clauses)] if optional_at_least_one and at_least_one_action_clauses else [])

    return all_clauses


def starting_state_clauses(pegs, empty_hole, N):
    starting_state_clauses = []
    for hole in range(1, N + 1):
        peg_id = pegs.get((hole, 1))
        if hole == empty_hole:
            starting_state_clauses.append(f"-{peg_id}")
        else:
            starting_state_clauses.append(f"{peg_id}")
    return starting_state_clauses


def ending_state_clauses(pegs, N):
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


def main():
    N, empty_hole, triples = read_input()
    expanded_triples = triples + [(C, B, A) for A, B, C in triples]
    peg, jump = assign_ids(N, expanded_triples)
    
    clauses = precondition_axioms(N, expanded_triples, peg, jump)
    causal_clauses = causal_axioms(N, expanded_triples, peg, jump)
    frame_clauses = frame_axioms(N, expanded_triples, peg, jump)
    exclusive_action_clauses = time_clauses(N, jump)
    starting_state = starting_state_clauses(peg, empty_hole, N)
    ending_state = ending_state_clauses(peg, N)

    all_clauses = clauses + causal_clauses + frame_clauses + exclusive_action_clauses + starting_state + ending_state
    
    legend = create_legend(peg, jump)
    
    with open('front_end_output.txt', 'w') as file:
        for clause in all_clauses:
            file.write(f"{clause}\n")
        
        file.write("0\n")
        for id, desc in sorted(legend.items()):
            file.write(f"{id} {desc}\n")

main()


