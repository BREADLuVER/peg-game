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

def read_input(filename):
    with open(filename, 'r') as file:
        n, _ = map(int, file.readline().strip().split())
        triples = [tuple(map(int, line.strip().split())) for line in file]
    return n, triples

def peg_index(hole, time, n):
    return (hole - 1) * (n - 1) + time

def jump_index(start, over, end, time, n, triples):
    base = n * (n - 1)
    jump_order = [(start, over, end) for start, over, end in triples]
    return base + jump_order.index((start, over, end)) * (n - 2) + time

def generate_cnf_clauses(n, triples):
    clauses = []
    for time in range(1, n - 1):
        for start, over, end in triples:
            jump_num = jump_index(start, over, end, time, n, triples)
            preconditions = [
                peg_index(start, time, n),
                peg_index(over, time, n),
                -peg_index(end, time, n)
            ]
            causal = [
                -peg_index(start, time + 1, n),
                -peg_index(over, time + 1, n),
                peg_index(end, time + 1, n)
            ]
            for pre in preconditions:
                clauses.append(f"-{jump_num} {pre}")
            for cause in causal:
                clauses.append(f"-{jump_num} {cause}")
    for hole in range(1, n + 1):
        if hole == 1:
            clauses.append(f"-{peg_index(hole, 1, n)}")
        else:
            clauses.append(f"{peg_index(hole, 1, n)}")
    ending_clause = " ".join([str(peg_index(hole, n - 1, n)) for hole in range(1, n + 1)])
    clauses.append(ending_clause)
    return clauses

def print_cnf_clauses_to_file(clauses, filename):
    with open(filename, 'w') as f:
        for clause in clauses:
            f.write(f"{clause}\n")
        f.write("0\n")
        for i in range(1, 29):
            if i <= 16:
                f.write(f"{i} Jump({(i-1)//4+1},{((i-1)%4)//2+1},{((i-1)%2)+1},{(i+1)//2})\n")
            else:
                f.write(f"{i} Peg({(i-17)//3+1},{(i-17)%3+1})\n")

def main():
    input_filename = 'game_board_input.txt'
    output_filename = 'clauses_output.txt'
    n, triples = read_input(input_filename)
    clauses = generate_cnf_clauses(n, triples)
    print_cnf_clauses_to_file(clauses, output_filename)

main()