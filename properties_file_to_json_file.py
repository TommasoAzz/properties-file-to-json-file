from string import Template
import sys
import os
import constant


# Gets the file name passed as argument to the script. Raises an exception if the argument is not given.
def get_file_name() -> str:
    if len(sys.argv) < 2:
        raise EnvironmentError("File name not inserted.")
    return sys.argv[1]


# Checks if the file passed as argument exists.
def check_file_existence(file_name: str) -> bool:
    return os.path.isfile(file_name)


# Returns information from the row (which should have the format of string_with_no_spaces=string_eventually_with_spaces) and if there was an empty line.
def extract_information_from_row(row: str):
    empty_line = 0
    if len(row.strip()) == 0:
        empty_line = 1
        return constant.WRONG_INPUT, constant.WRONG_INPUT, empty_line
    if len(row.split("=")) != 2:
        print(f"Row with content:\n{row}\nis not in the specified format.")
        return constant.WRONG_INPUT, constant.WRONG_INPUT, empty_line
    items = row.split("=")
    return items[0].replace(" ", "").strip(), items[1].strip(), empty_line


# Given a file name (with single extension), a list of keys (ordered like in the file in which they came from),
# a list of values (ordered like in the file in which they came from),
# creates the content string to write to write to the output file later.
# Returns the file name (first argument) and the file content.
def create_file_content(file_name: str, keys: list, values: list):
    out_file_name = file_name[0:file_name.index(".")]
    out_file_name = out_file_name.lower()
    out_file_name = out_file_name.replace("_", "")
    out_file_name = out_file_name.replace("-", "")

    # File header
    file_content = "{\n"

    # Class content
    for i in range(0, len(keys)):
        file_content += return_spaces(4)
        template = Template("\"$key\": \"$value\",\n")
        file_content += template.substitute(key=keys[i], value=values[i])

    # Removing trailing comma
    file_content = file_content[0:len(file_content) - 2]

    # File footer
    file_content += "\n}"

    return out_file_name, file_content


# Returns a string consisting in number spaces.
def return_spaces(number: int):
    spaces = ""

    for i in range(0, number):
        spaces += " "

    return spaces


# Writes the content into a file named file_name with extension .dart.
def write_content_to_file(file_name: str, content: str):
    template = Template("$fn.json")
    new_file = open(template.substitute(fn=file_name), "w")
    new_file.write(content)
    new_file.close()


# Main function definition
def main():
    try:
        name = get_file_name()
        print(f"Converting file: {name}")
        if not check_file_existence(name):
            raise FileNotFoundError(f"The file with name {name} was not found.")

        with open(name, 'r') as input_file:
            rows = input_file.readlines()
            keys = []
            values = []
            empty_lines = 0
            for row in rows:
                new_key, new_value, empty_line = extract_information_from_row(row)
                keys.append(new_key)
                values.append(new_value)
                empty_lines += empty_line
            keys = list(filter(constant.WRONG_INPUT.__ne__, keys))
            values = list(filter(constant.WRONG_INPUT.__ne__, values))
            file_name, file_content = create_file_content(name, keys, values)

            write_content_to_file(file_name, file_content)
            print("Done. " + f"{empty_lines} empty lines were not considered." if empty_lines > 0 else "")
    except FileNotFoundError:
        print("The file was not found.")
    except EnvironmentError:
        print("The file name was not inserted. The script cannot continue.")


main()
