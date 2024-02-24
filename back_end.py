def read_dp_output(filename):
    assignments = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if parts[0] == '0':
                break
            var, val = int(parts[0]), parts[1]
            assignments.append((var, val))
    return assignments

def decode_action(var):
    action_mapping = {
        6: "Jump(1,2,3,1)",
    }
    return action_mapping.get(var, "Unknown action")

def apply_move(game_state, move):
    return game_state

def translate_to_moves(assignments):
    moves = []
    game_state = {}
    for var, val in assignments:
        if val == 'T':
            action = decode_action(var)
            if action != "Unknown action":
                game_state = apply_move(game_state, action)
                moves.append(action)
    return moves

def main(dp_output_filename):
    assignments = read_dp_output(dp_output_filename)
    moves = translate_to_moves(assignments)
    print("Sequence of Moves to Solve the Peg Game:")
    for move in moves:
        print(move)

dp_output_filename = 'dp_output.txt'
main(dp_output_filename)

