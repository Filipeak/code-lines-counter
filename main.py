import os
import json

CONFIG_FILE_NAME = "counter_config.json"

data_list = []


class Data:
    def __init__(self, name, path, extensions):
        self.name = name
        self.path = path
        self.extensions = extensions


class Option:
    def __init__(self, name, action):
        self.name = name
        self.action = action


def get_files(dir_name, extensions):
    if not os.path.isdir(dir_name):
        print(dir_name + " is not a directory!")
        return []

    files = os.listdir(dir_name)
    all_files = list()

    for file in files:
        full_path = os.path.join(dir_name, file)

        if os.path.isdir(full_path):
            all_files = all_files + get_files(full_path, extensions)
        else:
            ext = os.path.splitext(full_path)[1]

            if ext in extensions:
                all_files.append(full_path)

    return all_files


def get_lines_count_in_file(file_path):
    try:
        with open(file_path, "r") as file:
            return len(file.readlines())
    except UnicodeDecodeError as error:
        return 0


def count_all_lines(dir_name, extensions):
    files = get_files(dir_name, extensions)
    total_lines = 0

    for file in files:
        total_lines += get_lines_count_in_file(file)

    return total_lines


def load_data():
    if not os.path.isfile(CONFIG_FILE_NAME):
        save_data()

    with open(CONFIG_FILE_NAME, "r") as file:
        file_text = file.read()

        if file_text == "" or file_text is None:
            return

        global data_list

        data = json.loads(file_text)

        data_list = [Data(d["name"], d["path"], d["extensions"]) for d in data]


def save_data():
    with open(CONFIG_FILE_NAME, "w") as file:
        file.write(json.dumps([d.__dict__ for d in data_list]))


def add_config_option():
    name = input("Enter name: ")
    path = input("Enter path: ")
    extensions = input("Enter extensions (seperated by ';'): ").split(';')

    if not name or not path or not extensions:
        print("Values cannot be empty!")
        return

    data_list.append(Data(name, path, extensions))
    save_data()

    print("Successfully added new config!")


def delete_config_option():
    try:
        index = int(input("Enter Index: "))
    except ValueError:
        print("Invalid index! Try again...")
        return

    if 0 <= index < len(data_list):
        data_list.remove(data_list[index])
        save_data()

        print("Successfully deleted config!")
    else:
        print("Invalid index! Try again...")


def view_config_option():
    try:
        index = int(input("Enter Index: "))
    except ValueError:
        print("Invalid index! Try again...")
        return

    if 0 <= index < len(data_list):
        print("Name: " + data_list[index].name)
        print("Path: " + data_list[index].path)
        print("Extensions: ")

        for ext in data_list[index].extensions:
            print("  - " + ext)

    else:
        print("Invalid index! Try again...")


def manual_option():
    path = input("Enter path: ")
    extensions = input("Enter extensions (seperated by ';'): ").split(';')

    if not path or not extensions:
        print("Values cannot be empty!")
        return

    print(count_all_lines(path, extensions))


def main():
    data_list.clear()

    load_data()

    print("\n")
    print("========== LINE COUNTER ==========")

    options = [
        Option("Add Config", add_config_option),
        Option("Delete Config", delete_config_option),
        Option("View Config", view_config_option),
        Option("Manual", manual_option)
    ]

    for data in data_list:
        options.append(Option(data.name, lambda: print(count_all_lines(data.path, data.extensions))))

    i = 1
    data_index = -1

    for option in options:
        iterating_data = i == 4 + 1

        if iterating_data:
            data_index += 1
            print(" - Configs")

        print(f"{i}. {option.name} {str(data_index) if iterating_data else ''}")

        i += 1

    try:
        selected_option_index = int(input("Enter option: "))
    except ValueError:
        print("Invalid option! Try again...")
        return

    if 0 < selected_option_index <= len(options):
        option = options[selected_option_index - 1]

        print("")

        option.action()
    else:
        print("Invalid option! Try again...")


while True:
    main()
