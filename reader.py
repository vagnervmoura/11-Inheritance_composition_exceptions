# python reader.py in.csv out.json 1,1,cat 0,1,dog 2,1,bread
# python reader.py in.lsk out.lsk 1,1,cat 0,1,dog 2,1,bread
# python reader.py in.lsk out2.pickle 1,1,cat 0,1,dog 2,1,bread
# python reader.py in.lsk out2.lsk 1,1,cat 0,1,dog 2,1,bread
# python reader.py in.lsk out3.pickle 1,1,cat 0,1,dog 2,1,bread
# python reader.py in.lsk out3.pickle 1,1,cat 0,1,dog 2,1000,bread   ----   This one will make error, try to create exceptions for this in change_content

import sys
import csv
import pickle

class InputArguments:
    def __init__(self, args):
        self.input_file = args[0]
        self.output_file = args[1]
        self.changes = args[2:] if len(args) > 2 else []
        self.changes = [
            (
                int(a.split(",")[0]),
                int(a.split(",")[1]),
                a.split(",")[2]
            )
            for a in self.changes
        ]

    def __str__(self):
        return (f"Read from: {self.input_file}\n"
                f"Save to: {self.output_file}\n"
                f"Changes: {self.changes}"
                )


class BaseFileHandler:
    def __init__(self, file_name):
        self.file_name = file_name


class PickleFileHandler(BaseFileHandler):
    def read(self):
        with open(self.file_name, "ab") as f:
            pass

        with open(self.file_name, "rb") as f:
            print("Teste")
            content = pickle.load(f)
        return content

    def write(self, content):
        #with open(self.file_name, "ab") as f:
        #    pass

        with open(self.file_name, "wb") as f:
            pickle.dump(content, f)


class CSVFileHandler(BaseFileHandler):
    def read(self):
        with open(self.file_name, "a") as f:
            pass

        with open(self.file_name, "r") as f:
            content = list(csv.reader(f))
        return content

    def write(self, content):
        with open(self.file_name, "a") as f:
            pass

        with open(self.file_name, "w", newline='') as f:
            csv.writer(f).writerows(content)


class JSONFileHandler(BaseFileHandler):
    pass


def change_content(content, changes):
    for change in changes:
        if isinstance(change, tuple):
            x, y, v = change
        else:
            x, y, v = map(int, change.split(","))

        while len(content) <= y:
            content.append([])  # Adiciona novas linhas, se necessário

        while len(content[y]) <= x:
            content[y].append(None)  # Adiciona novos elementos na linha, se necessário

        content[y][x] = v


    #for change in changes:
    #    x, y, v = map(int, change.split(","))
    #
    #    while len(content) <= y:
    #        content.append([])  # Adiciona novas linhas, se necessário
    #
    #    while len(content[y]) <= x:
    #        content[y].append(None)  # Adiciona novos elementos na linha, se necessário
    #
    #    content[y][x] = v


    #for(x, y, v) in changes:
    #    while len(content) <= x:
    #        content.append([]) # Add new rows if necessary
    #
    #    while len(content[x]) <= y:
    #        content[x].append(None) # Add new elements on row, if necessary
    #
    #    content[x][y] = v

        #if 0 <= x < len(content) and 0 <= y < len(content[x]):
        #    content[x][y] = v
        #else:
        #    print(f"WARNING: Ignored change at ({x}, {y}, {v}). Index out of range.")
    return content

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("ERROR: too few arguments.")
        sys.exit()

    if len(sys.argv) < 4:
        print("WARNING: No changes are present in the command...")
        sys.exit()

    arguments = InputArguments(sys.argv[1:])

    # Select the proper handler for the INPUT file
    if arguments.input_file.endswith(".pickle"):
        input_file_handler = PickleFileHandler
    elif arguments.input_file.endswith(".csv"):
        input_file_handler = CSVFileHandler
    elif arguments.input_file.endswith(".json"):
        input_file_handler = JSONFileHandler
    else:
        raise NotImplementedError("Program handles only PICKLE, CSV and JSON files.")

    # Select the proper handler for the OUTPUT file
    if arguments.output_file.endswith(".pickle"):
        output_file_handler = PickleFileHandler
    elif arguments.output_file.endswith(".csv"):
        output_file_handler = CSVFileHandler
    elif arguments.output_file.endswith(".json"):
        output_file_handler = JSONFileHandler
    else:
        raise NotImplementedError("Program handles only PICKLE, CSV and JSON files.")

    print(arguments)

    input_file_handler = input_file_handler(arguments.input_file)
    output_file_handler = output_file_handler(arguments.output_file)

    content = input_file_handler.read()

    print(f"BEFORE: {content}")
    content = change_content(content, arguments.changes)
    print(f"AFTER: {content}")

    output_file_handler.write(content)