import utils

class FileSaver():
    def __init__(self):
        pass

    def save_values_in_dimacs(self, values: dict, file_name: str):
        output_file = open(file_name, "w")
        output_file.write(f'p cnf {len(values.keys())} {len(values.keys())}\n')

        for value_key, value in values.items():
            line_str = str(value_key)
            if not value:
                line_str = "-" + line_str
            
            output_file.write(f'{line_str} 0\n')

        output_file.close()