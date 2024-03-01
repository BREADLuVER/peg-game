def parse_input(input_filename):
    with open(input_filename, 'r') as file:
        lines = file.readlines()
        clauses = []
        for line in lines:
            if line.strip() == '0':
                break
            clause = list(map(int, line.split()))
            clauses.append(clause)
        max_atom = max(abs(lit) for clause in clauses for lit in clause)
        return clauses, max_atom

def davis_putnam(clauses, max_atom, assignments={}, atom=1):
    if not clauses:
        for a in range(atom, max_atom + 1):
            if a not in assignments:
                assignments[a] = True
        return assignments
    if any(not clause for clause in clauses):
        return None

    _, literal = min((len([lit for lit in clause if abs(lit) == abs(clause[0])]), clause[0]) for clause in clauses)
    print(f'Selected literal: {literal}')  # Debug print

    new_clauses = simplify(clauses, literal)
    result = davis_putnam(new_clauses, max_atom, {**assignments, abs(literal): literal > 0}, atom + 1)
    if result is not None:
        return result

    new_clauses = simplify(clauses, -literal)
    return davis_putnam(new_clauses, max_atom, {**assignments, abs(literal): literal < 0}, atom + 1)

def solve_sat_from_file(input_filename, output_filename):
    clauses, max_atom = parse_input(input_filename)
    solution = davis_putnam(clauses, max_atom)
    print(f'Solution: {solution}')  # Debug print
    write_output(output_filename, solution)

def simplify(clauses, literal):
    clauses = [clause for clause in clauses if literal not in clause]
    return [[lit for lit in clause if lit != -literal] for clause in clauses]

#ss
def write_output(output_filename, solution):
    with open(output_filename, 'w') as file:
        if solution is None:
            file.write('0\n')
        else:
            for atom, value in solution.items():
                file.write(f'{atom} {"T" if value else "F"}\n')
            file.write('0\n')

input_filename = 'front_end_output.txt'
output_filename = 'dp_output.txt'
solve_sat_from_file(input_filename, output_filename)
