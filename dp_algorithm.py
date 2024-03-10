def parse_input(input_filename):
    with open(input_filename, 'r') as file:
        content = file.read()
    separator_index = content.find('\n0\n')

    if separator_index != -1:
        clause_part, legend_part = content.split('\n0\n')
        clause_lines = clause_part.strip().splitlines()
        legend_lines = legend_part.strip().splitlines()
    else:
        clause_lines = content.strip().splitlines()
        legend_lines = []

    clauses = [list(map(int, line.split())) for line in clause_lines if line.strip()]
    all_atoms = set(abs(lit) for clause in clauses for lit in clause)
    legend_lines = legend_part.strip().splitlines()
    legends = {int(line.split()[0]): ' '.join(line.split()[1:]) for line in legend_lines}
    return clauses, all_atoms, legends

def davis_putnam(clauses, assignments={}):
    # Base case checks
    if not clauses:
        return True, assignments
    if any(len(clause) == 0 for clause in clauses):
        return False, {}
    
    # Proactively resolve literals that can directly satisfy single-instance clauses
    for literal in get_all_literals(clauses, assignments):
        if can_directly_resolve(clauses, literal):
            value = get_direct_resolution_value(clauses, literal)
            assignments[literal] = value
            new_clauses = apply_assignment(clauses, literal, value)
            result, final_assignments = davis_putnam(new_clauses, assignments)
            if result:
                return True, final_assignments
            else:
                del assignments[literal]  # Backtrack on this assignment

    # If no single-instance resolution is possible, proceed with the standard assignment
    literal = select_literal(clauses, assignments)
    for value in [True, False]:
        new_assignments = assignments.copy()
        new_assignments[literal] = value
        new_clauses = apply_assignment(clauses, literal, value)
        result, final_assignments = davis_putnam(new_clauses, new_assignments)
        if result:
            return True, final_assignments
    
    return False, {}

def select_literal(clauses, assignments):
    """
    Selects the next literal to assign, avoiding those already assigned.
    """
    for clause in clauses:
        for lit in clause:
            if abs(lit) not in assignments:
                return abs(lit)
    return None 


def get_all_literals(clauses, assignments):
    """Returns a set of all literals not yet assigned."""
    literals = set()
    for clause in clauses:
        for lit in clause:
            if abs(lit) not in assignments:
                literals.add(abs(lit))
    return literals

def can_directly_resolve(clauses, literal):
    """Check if assigning a literal can directly resolve a single-instance clause."""
    for clause in clauses:
        if literal in clause or -literal in clause:
            if all(abs(lit) == literal for lit in clause):
                return True
    return False

def get_direct_resolution_value(clauses, literal):
    """Determines the value to assign to a literal to resolve a single-instance clause."""
    for clause in clauses:
        if literal in clause or -literal in clause:
            if all(abs(lit) == literal for lit in clause):
                return literal in clause
    return None

def apply_assignment(clauses, literal, value):
    """Simplifies clauses based on a given assignment."""
    new_clauses = []
    for clause in clauses:
        if (literal in clause and value) or (-literal in clause and not value):
            continue  # Clause is satisfied
        new_clause = [lit for lit in clause if abs(lit) != literal]
        new_clauses.append(new_clause)
    return new_clauses

def arbitrary_assign(solution_assignments, legends):
    # Check for missing cases in solution_assignments based on legends
    for atom in legends.keys():
        if atom not in solution_assignments:
            # If missing, assign it True (T)
            solution_assignments[atom] = 'T'


def solve_sat_from_file(input_filename, output_filename):
    clauses, all_atoms, legends = parse_input(input_filename)
    solution_exists, solution_assignments = davis_putnam(clauses)
    if solution_exists:
        # Fill in any missing assignments based on legends
        arbitrary_assign(solution_assignments, legends)
        print(f'Solution Exists: {solution_exists}')

    write_output(output_filename, solution_assignments if solution_exists else None, legends)


def write_output(output_filename, solution, legends):
    with open(output_filename, 'w') as file:
        if solution is None:
            file.write("0\n No solution found.\n")
        else:
            for atom, value in sorted(solution.items()):  # Optionally sort by atom for consistent output
                file.write(f'{atom} {"T" if value else "F"}\n')
            file.write(f'0\n')  # You may remove this line if '0' is no longer needed as an end-of-file marker.
            for k, v in legends.items():
                file.write(f'{k} {v}\n')

input_filename = 'front_end_output.txt'
output_filename = 'dp_output.txt'
solve_sat_from_file(input_filename, output_filename)
