def read_game_board(filename):
    with open(filename, 'r') as file:
        first_line = file.readline().strip().split()
        num_holes, initial_empty = int(first_line[0]), int(first_line[1])
        triples = [tuple(map(int, line.strip().split())) for line in file]
    return num_holes, initial_empty, triples

def encode_state_or_action(item, encoding_map, counter):
    if item not in encoding_map:
        encoding_map[item] = counter
        counter += 1
    return encoding_map[item], counter

def generate_encoded_clauses(triples, num_holes, initial_empty):
    encoding_map = {}
    clauses = []
    counter = 1
    for i in range(1, num_holes + 1):
        item = f"Peg({i},1)"
        identifier, counter = encode_state_or_action(item, encoding_map, counter)
        if i == initial_empty:
            clauses.append(f"-{identifier}")
        else:
            clauses.append(f"{identifier}")
    for a, b, c in triples:
        for t in range(1, num_holes - 1):
            jump_item = f"Jump({a},{b},{c},{t})"
            peg_a_item = f"Peg({a},{t})"
            peg_b_item = f"Peg({b},{t})"
            peg_c_item = f"Peg({c},{t})"
            jump_id, counter = encode_state_or_action(jump_item, encoding_map, counter)
            peg_a_id, counter = encode_state_or_action(peg_a_item, encoding_map, counter)
            peg_b_id, counter = encode_state_or_action(peg_b_item, encoding_map, counter)
            peg_c_id, counter = encode_state_or_action(peg_c_item, encoding_map, counter)
            clauses.append(f"-{jump_id} {peg_a_id}")
            clauses.append(f"-{jump_id} {peg_b_id}")
            clauses.append(f"-{jump_id} -{peg_c_id}")
    return clauses, encoding_map

def write_clauses_to_file(clauses, filename):
    with open(filename, 'w') as file:
        for clause in clauses:
            file.write(f"{clause}\n")
        file.write("0\n")

def main(input_filename, output_filename):
    num_holes, initial_empty, triples = read_game_board(input_filename)
    clauses, encoding_map = generate_encoded_clauses(triples, num_holes, initial_empty)
    write_clauses_to_file(clauses, output_filename)

input_filename = 'game_board_input.txt'
output_filename = 'clauses_output.txt'
main(input_filename, output_filename)


