def parse_input(input_filename):
    with open(input_filename, 'r') as file:
        lines = file.readlines()
        separator_index = lines.index("0\n") if "0\n" in lines else None

        if separator_index is not None:
            clause_lines = lines[:separator_index]
            legend_lines = lines[separator_index + 1:]
        else:
            clause_lines = lines
            legend_lines = []

        clauses = [list(map(int, line.split())) for line in clause_lines if line.strip()]
        all_atoms = set(abs(lit) for clause in clauses for lit in clause)
        legends = [line.strip() for line in legend_lines if line.strip()]

    return clauses, all_atoms, legends

def davis_putnam(clauses, all_atoms, assignments={}):
    # Base case checks
    if not clauses or all(atom in assignments for atom in all_atoms):
        for atom in all_atoms:
            if atom and atom not in assignments:
                assignments[atom] = True
        return True, assignments
    if any(len(clause) == 0 for clause in clauses):
        return False, {}

    # Assign pure literals
    clauses, assignments = assign_pure_literals(clauses, assignments)

    # Proactively resolve literals that can directly satisfy single-instance clauses
    for literal in get_all_literals(clauses, assignments):
        if can_directly_resolve(clauses, literal):
            value = get_direct_resolution_value(clauses, literal)
            assignments[literal] = value
            new_clauses = apply_assignment(clauses, literal, value)
            result, final_assignments = davis_putnam(new_clauses, all_atoms, assignments)
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
        result, final_assignments = davis_putnam(new_clauses, all_atoms, new_assignments)
        if result:
            return True, final_assignments

    return False, {}

def assign_pure_literals(clauses, assignments):
    literal_polarity = {}
    for clause in clauses:
        for lit in clause:
            if abs(lit) in assignments:  # Skip if already assigned
                continue
            if abs(lit) not in literal_polarity:
                literal_polarity[abs(lit)] = lit > 0
            else:
                # If we see the opposite polarity, set to None indicating it's not pure
                if literal_polarity[abs(lit)] != (lit > 0):
                    literal_polarity[abs(lit)] = None

    # Assign pure literals
    for lit, is_positive in literal_polarity.items():
        if is_positive is not None:  # None indicates it's not pure
            assignments[lit] = is_positive
            clauses = apply_assignment(clauses, lit, is_positive)
    return clauses, assignments

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

def select_literal(clauses, assignments):
    """Selects the next literal to assign, avoiding those already assigned."""
    for clause in clauses:
        for lit in clause:
            if abs(lit) not in assignments:
                return abs(lit)
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

def solve_sat_from_file(input_filename, output_filename):
    clauses, all_atoms, legends = parse_input(input_filename)
    solution_exists, solution_assignments = davis_putnam(clauses, all_atoms)
    print(f'Solution Exists: {solution_exists}')
    write_output(output_filename, solution_assignments if solution_exists else None, legends)

def write_output(output_filename, solution, legends):
    with open(output_filename, 'w') as file:
        if solution is None:
            file.write("No solution found.\n")
        else:
            filtered_solution = {k: v for k, v in solution.items() if k is not None and v is not None}
            for atom, value in sorted(filtered_solution.items()):
                file.write(f'{atom} {"T" if value else "F"}\n')
            file.write('0\n')  # Separator before the legends section
            for legend in legends:
                file.write(f'{legend}\n')  # Write each legend


input_filename = 'front_end_output.txt'
output_filename = 'dp_output.txt'
solve_sat_from_file(input_filename, output_filename)
