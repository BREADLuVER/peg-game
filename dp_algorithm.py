import math

def parse_input(input_filename):
    with open(input_filename, 'r') as file:
        content = file.read()
    separator_index = content.find('\n0\n')

    # Initialize legend_part as an empty string
    legend_part = ''

    # Split the content into clauses and legends
    if separator_index != -1:
        clause_part, legend_part = content.split('\n0\n')
        clause_lines = clause_part.strip().splitlines()
    else:
        clause_lines = content.strip().splitlines()

    # Remove '0's from clauses
    clauses = [list(map(int, line.split())) for line in clause_lines if line.strip() and line != '0']
    all_atoms = set(abs(lit) for clause in clauses for lit in clause if lit != 0)
    legend_lines = legend_part.strip().splitlines()
    legends = {int(line.split()[0]): ' '.join(line.split()[1:]) for line in legend_lines if line.strip() and line.split()[0] != '0'}
    return clauses, all_atoms, legends


def find_unit_clauses(clauses):
    """Finds unit clauses in the clauses."""
    return [clause[0] for clause in clauses if len(clause) == 1]


def find_pure_literals(clauses):
    """Finds pure literals in the clauses."""
    positive = set()
    negative = set()
    for clause in clauses:
        for lit in clause:
            if lit > 0:
                positive.add(lit)
            else:
                negative.add(-lit)
    # pure literals are those that are in positive or negative but not both
    pure_literals = {lit for lit in positive if lit not in negative} | {-lit for lit in negative if lit not in positive}
    return pure_literals


def davis_putnam(clauses, assignments={}, tried_assignments=None, call_limit=200, current_call=0):
    if tried_assignments is None:
        tried_assignments = set()

    # base conditions
    if not clauses:
        print("Solution found with no clauses left.")
        return True, assignments
    if any(len(clause) == 0 for clause in clauses):
        print("Empty clause found, no solution possible.")
        return False, {}
    
    if current_call >= call_limit: # limit the number of recursive calls incase base checks fails
        return False, {}
    
    current_call+=1
    # check for unit clauses
    unit_clauses = find_unit_clauses(clauses)
    for literal in unit_clauses:
        if abs(literal) not in assignments:
            assignments[abs(literal)] = True if literal > 0 else False
            clauses = apply_assignment(clauses, abs(literal), assignments[abs(literal)])
            if not clauses:
                return True, assignments
            if any(len(clause) == 0 for clause in clauses):
                return False, {}

    # check for pure literals
    pure_literals = find_pure_literals(clauses)
    #print(f"Checking for pure literals. Current assignments: {assignments}")
    for literal in pure_literals:
        if abs(literal) not in assignments:
            assignments[abs(literal)] = True if literal > 0 else False
            clauses = apply_assignment(clauses, abs(literal), assignments[abs(literal)])
            if not clauses:
                return True, assignments
            if any(len(clause) == 0 for clause in clauses):
                return False, {}

    # standard DPLL
    if clauses:
        literal = select_literal(clauses, assignments)
        for value in [True, False]:
            if (literal, value) in tried_assignments: # keep a tried_assignment to skip assignments that have already been tried
                continue
            new_assignments = assignments.copy()
            new_assignments[literal] = value
            new_clauses = apply_assignment(clauses, literal, value)
            if any(len(clause) == 0 for clause in new_clauses):
                continue
            new_tried_assignments = tried_assignments.copy()  # copy tried_assignments for the recursive call
            new_tried_assignments.add((literal, value))
            result, final_assignments = davis_putnam(new_clauses, new_assignments, new_tried_assignments, call_limit, current_call)
            if result:
                return True, final_assignments

    return False, {}


def select_literal(clauses, assignments):
    """selects an unassigned literal from the clauses."""
    for clause in clauses: # check for unassigned literals in each clause
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
    """vheck if assigning a literal can directly resolve a single-instance clause."""
    for clause in clauses:
        if literal in clause or -literal in clause:
            if all(abs(lit) == literal for lit in clause):
                return True
    return False

def get_direct_resolution_value(clauses, literal):
    """determines the value to assign to a literal to resolve a single-instance clause."""
    for clause in clauses:
        if literal in clause or -literal in clause:
            if all(abs(lit) == literal for lit in clause):
                return literal in clause
    return None

def apply_assignment(clauses, literal, value):
    """simplifies clauses based on a given assignment."""
    new_clauses = []
    for clause in clauses:
        if (literal in clause and value) or (-literal in clause and not value):
            continue  # Clause is satisfied, so it is removed from the list
        new_clause = [lit for lit in clause if abs(lit) != literal]

        new_clauses.append(new_clause)
    return new_clauses

def arbitrary_assign(solution_assignments, legends):
    """Fills in any missing assignments based on legends."""
    for atom in legends.keys():
        if atom not in solution_assignments:
            solution_assignments[atom] = 'T'


def solve_sat_from_file(input_filename, output_filename):
    clauses, all_atoms, legends = parse_input(input_filename)
    solution_exists, solution_assignments = davis_putnam(clauses,  call_limit=int(math.sqrt(len(legends))))
    if solution_exists:
        arbitrary_assign(solution_assignments, legends)
    write_output(output_filename, solution_assignments if solution_exists else None, legends)


def write_output(output_filename, solution, legends):
    with open(output_filename, 'w') as file:
        if solution is None:
            file.write("0\n")
            for k, v in legends.items():
                file.write(f'{k} {v}\n')
        else:
            for atom, value in sorted(solution.items()):  # Optionally sort by atom for consistent output
                file.write(f'{atom} {"T" if value else "F"}\n')
            file.write(f'0\n')  # You may remove this line if '0' is no longer needed as an end-of-file marker.
            for k, v in legends.items():
                file.write(f'{k} {v}\n')


input_filename = 'front_end_output.txt'
output_filename = 'dp_output.txt'
solve_sat_from_file(input_filename, output_filename)

