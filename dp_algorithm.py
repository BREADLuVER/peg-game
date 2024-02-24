def dp_solve(clauses, assignment=[]):
    clauses, assignment = simplify(clauses, assignment)
    if not clauses:
        return assignment
    if any(not clause for clause in clauses):
        return None
    variable = choose_variable(clauses)
    if solution := dp_solve(assign(clauses, variable, True), assignment + [(variable, True)]):
        return solution
    return dp_solve(assign(clauses, variable, False), assignment + [(variable, False)])

def simplify(clauses, assignment):
    true_literals = {var if value else -var for var, value in assignment}
    simplified_clauses = []
    for clause in clauses:
        if any(literal in true_literals for literal in clause):
            continue
        simplified_clause = [literal for literal in clause if -literal not in true_literals]
        simplified_clauses.append(simplified_clause)
    return simplified_clauses, assignment

def choose_variable(clauses):
    from collections import Counter
    all_literals = [abs(literal) for clause in clauses for literal in clause]
    most_common_var, _ = Counter(all_literals).most_common(1)[0]
    return most_common_var

def assign(clauses, variable, value):
    new_assignment = [(variable, value)]
    return simplify(clauses, new_assignment)[0]

def read_clauses_and_legend_from_file(filename):
    clauses = []
    legend = {}
    reading_clauses = True
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line == '0':  
                reading_clauses = False
                continue
            if reading_clauses:
                clause = list(map(int, line.split()))
                clauses.append(clause)
            else:
                var, description = line.split(maxsplit=1)
                legend[int(var)] = description
    return clauses, legend

def write_solution_and_legend_to_file(solution, legend, filename):
    with open(filename, 'w') as file:
        if solution is None:
            file.write('0\n')
        else:
            for var, val in solution:
                file.write(f"{var} {'T' if val else 'F'}\n")
        file.write('0\n')  
        for var, desc in legend.items():
            file.write(f"{var} {desc}\n")

def solve_sat_from_file(input_filename, output_filename):
    clauses, legend = read_clauses_and_legend_from_file(input_filename)
    solution = dp_solve(clauses)
    write_solution_and_legend_to_file(solution, legend, output_filename)

input_filename = 'clauses_output.txt'
output_filename = 'dp_output.txt'
solve_sat_from_file(input_filename, output_filename)
