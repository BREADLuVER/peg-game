def read_game_board(filename):
    with open(filename, 'r') as file:
        first_line = file.readline().strip().split()
        num_holes, initial_empty = int(first_line[0]), int(first_line[1])
        triples = [tuple(map(int, line.strip().split())) for line in file]
    return num_holes, initial_empty, triples
