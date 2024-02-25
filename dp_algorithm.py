def read_clauses_and_legend_from_file(filename):
    clauses = []
    back_matter = ''
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
                back_matter += line + '\n'
    return clauses, back_matter

def apply_unit_clause(clauses, unit):
    new_clauses = []
    for clause in clauses:
        if unit in clause:
            continue
        if -unit in clause:
            new_clause = [x for x in clause if x != -unit]
            new_clauses.append(new_clause)
        else:
            new_clauses.append(clause)
    return new_clauses

def apply_pure_literal_rule(clauses):
    new_clauses = []
    pure_literals = set()
    for clause in clauses:
        for literal in clause:
            if -literal not in pure_literals:
                pure_literals.add(literal)
    for clause in clauses:
        if not any(literal in pure_literals for literal in clause):
            new_clauses.append(clause)
    return new_clauses

def choose_literal(clauses):
    for clause in clauses:
        if clause:  # Ensure the clause is not empty
            for literal in clause:
                return literal
    return None

def assign(clauses, literal):
    new_clauses = []
    for clause in clauses:
        if literal in clause:
            continue
        if -literal in clause:
            new_clause = [x for x in clause if x != -literal]
            if not new_clause:  # Unsatisfiable if empty clause is produced
                return None
            new_clauses.append(new_clause)
        else:
            new_clauses.append(clause)
    return new_clauses

def dp_solve(clauses, assignments={}):
    # Base case: If there are no clauses left, a solution is found
    if not clauses:
        return assignments

    # If there's an empty clause, the problem is unsatisfiable
    if any(len(clause) == 0 for clause in clauses):
        return None

    # Unit clause propagation
    while any(len(clause) == 1 for clause in clauses):
        unit_clauses = [clause[0] for clause in clauses if len(clause) == 1]
        for unit in unit_clauses:
            assignments[abs(unit)] = (unit > 0)
            # Apply the unit clause to simplify the problem
            clauses = apply_unit_clause(clauses, unit)
            # Check for empty clauses again after applying unit clause
            if any(len(clause) == 0 for clause in clauses):
                return None

    # Choose a literal for branching
    literal = choose_literal(clauses)
    if literal is None:  # Safeguard check
        return assignments
    # Recursive case: Try assigning the chosen literal True, then False
    for val in [True, False]:
        new_assignments = assignments.copy()
        new_assignments[abs(literal)] = val
        new_clauses = assign(clauses, literal if val else -literal)
        result = dp_solve(new_clauses, new_assignments)
        if result is not None:
            return result  # Satisfiable with current assignment

    # If neither True nor False leads to a solution, the problem is unsatisfiable
    return None


def find_unit_clauses(clauses):
    """Finds all unit clauses in the current clause list."""
    return [clause[0] for clause in clauses if len(clause) == 1]

def write_solution_and_back_matter_to_file(solution, back_matter, filename):
    with open(filename, 'w') as file:
        if solution is None:
            file.write("No solution found.\n")  # Change this line to indicate unsatisfiability.
            print("No solution found.")  # Print to console as well.
        else:
            for var in sorted(solution):
                file.write(f"{var} {'T' if solution[var] else 'F'}\n")
            file.write('0\n')
        file.write(back_matter)


def solve_sat_from_file(input_filename, output_filename):
    clauses, back_matter = read_clauses_and_legend_from_file(input_filename)
    solution = dp_solve(clauses)
    write_solution_and_back_matter_to_file(solution, back_matter, output_filename)

# Example usage
input_filename = 'front_end_output.txt'
output_filename = 'dp_output.txt'
solve_sat_from_file(input_filename, output_filename)

