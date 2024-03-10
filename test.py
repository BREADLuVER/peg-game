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