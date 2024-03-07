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

def davis_putnam(clauses, assignments={}):
    # Simplify clauses and handle unit clauses
    clauses, changed = simplify_and_handle_unit_clauses(clauses)
    if changed:
        # If changes were made due to unit clauses, run DP again to check for further simplifications
        return davis_putnam(clauses, assignments)
    
    # If there are no clauses left, all have been satisfied
    if not clauses:
        return True, assignments
    
    # If there's an empty clause, a contradiction has occurred
    if any(len(clause) == 0 for clause in clauses):
        return False, {}
    
    # Select a literal for assignment (heuristic: first unassigned variable)
    literal = select_unassigned_literal(clauses, assignments)
    
    # Try assigning the literal True, then False if True fails
    for value in [True, False]:
        new_assignments = assignments.copy()
        new_assignments[abs(literal)] = value
        new_clauses = apply_assignment(clauses, literal, value)
        result, final_assignments = davis_putnam(new_clauses, new_assignments)
        if result:
            return True, final_assignments
    
    # If neither True nor False works for this literal, backtrack
    return False, {}

def simplify_and_handle_unit_clauses(clauses):
    """Simplify clauses by removing satisfied clauses and literals, handle unit clauses."""
    simplified_clauses = []
    assignments = {}
    changed = False

    # Detect unit clauses and assign values accordingly
    for clause in clauses:
        if len(clause) == 1:
            lit = clause[0]
            assignments[abs(lit)] = True if lit > 0 else False
            changed = True
    
    if not changed:
        return clauses, False
    
    # Apply found assignments to simplify clauses
    for clause in clauses:
        new_clause = []
        remove_clause = False
        for lit in clause:
            if abs(lit) in assignments:
                if (lit > 0 and assignments[abs(lit)]) or (lit < 0 and not assignments[abs(lit)]):
                    remove_clause = True
                    break
            else:
                new_clause.append(lit)
        if not remove_clause:
            simplified_clauses.append(new_clause)
    
    return simplified_clauses, True

def select_unassigned_literal(clauses, assignments):
    """Select the first unassigned literal."""
    for clause in clauses:
        for lit in clause:
            if abs(lit) not in assignments:
                return lit
    return None  # Should not happen if called correctly

def apply_assignment(clauses, literal, value):
    """Apply an assignment to simplify the set of clauses."""
    new_clauses = []
    for clause in clauses:
        # If the literal satisfies the clause, skip the clause
        if (literal in clause and value) or (-literal in clause and not value):
            continue
        # Otherwise, remove the literal if it appears in the clause
        new_clause = [lit for lit in clause if lit != literal and lit != -literal]
        new_clauses.append(new_clause)
    return new_clauses

def solve_sat_from_file(input_filename, output_filename):
    clauses, max_atom = parse_input(input_filename)
    solution = davis_putnam(clauses, max_atom)
    print(f'Solution: {solution}')
    write_output(output_filename, solution)

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
