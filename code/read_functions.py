import pandas as pd

def read_txt(file_path):
    data_list = []
    with open(file_path, 'r') as file:
        file_content = file.read()

    entries = file_content.split('\n\n')

    for entry in entries:

        entry_dict = {}
        entry_lines = entry.strip().split('\n')
        
        for line in entry_lines:

            parts = line.strip().split(':')
            if len(parts) == 2:
                column, value = parts[0].strip(), parts[1].strip()
                entry_dict[column] = value

        data_list.append(entry_dict)

    df = pd.DataFrame(data_list)

    return df
