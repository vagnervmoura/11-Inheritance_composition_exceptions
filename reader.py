# python .\reader.py source.json json_to.json "1,0,piano" "1,1,mug" "3,4,csv" "0,1,json" "3,3,pickle"
# python .\reader.py source.json json_to.csv "1,0,piano" "1,1,mug" "3,4,csv" "0,1,json" "3,3,pickle"
# python .\reader.py source.json json_to.pickle "1,0,piano" "1,1,mug" "3,4,csv" "0,1,json" "3,3,pickle

# python .\reader.py source.pickle pickle_to.pickle "1,0,piano" "1,1,mug" "3,4,csv" "0,1,json" "3,3,pickle"
# python .\reader.py source.pickle pickle_to.json "1,0,piano" "1,1,mug" "3,4,csv" "0,1,json" "3,3,pickle"
# python .\reader.py source.pickle pickle_to.csv "1,0,piano" "1,1,mug" "3,4,csv" "0,1,json" "3,3,pickle"

# python .\reader.py source.csv csv_to.csv "1,0,piano" "1,1,mug" "3,4,csv" "0,1,json" "3,3,pickle"
# python .\reader.py source.csv csv_to.pickle "1,0,piano" "1,1,mug" "3,4,csv" "0,1,json" "3,3,pickle"
# python .\reader.py source.csv csv_to.json "1,0,piano" "1,1,mug" "3,4,csv" "0,1,json" "3,3,pickle"

import sys
import csv
import pickle
import json

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
        try:
            with open(self.file_name, "rb") as f:
                content = pickle.load(f)
            return content
        except FileNotFoundError:
            print(f"WARNING: File {self.file_name} not found. Creating a new one with name {self.file_name}.")
            content = []
            self.write(content)
            return content
        except Exception as e:
            print(f"ERROR: Failed to read file {self.file_name}. Exception: {e}")
            sys.exit()

    def write(self, content):
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
    def read(self):
        try:
            with open(self.file_name, "r") as f:
                content = json.load(f)
            return content
        except FileNotFoundError:
            print(f"WARNING, File {self.file_name} not found. Creating a new one with name {self.file_name}.")
            content = []
            self.write(content)
            return content
        except Exception as e:
            print(f"ERROR: Failed to read file {self.file_name}. Exception: {e}")
            sys.exit()

    def write(self, content):
        with open(self.file_name, "w") as f:
            json.dump(content, f)



def change_content(content, changes):
    for change in changes:
        if isinstance(change, tuple):
            x, y, v = change
        else:
            x, y, v = map(int, change.split(","))

        while len(content) <= y:
            content.append([])  # Add new rows if necessary

        while len(content[y]) <= x:
            content[y].append(None)  # Add new elements on row, if necessary

        content[y][x] = v

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