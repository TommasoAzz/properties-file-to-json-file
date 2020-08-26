# properties-file-to-json-file

Utility Python script to convert a file with extension `.properties` (such as the configuration file `application.properties` in a Java Spring project) or a similar file, to a **JSON** file made of all string keys and string values.

## Requirements
**Python 3+**.

## How to run
Run the following command from a CLI:
```bash
python properties_file_to_json_file.py file_name_with_single_extension.properties
```
Please remove any leading dot, such in `.\file_name_with_single_extension.properties` otherwise the file will be named `.json`.

## Why .properties files?
Because I needed to parse `.properties` files 😎.  
Actually, the only requirement is that rows in the files are in the following format:
```
string_without_spaces=whatever string you like
```
All the rows that the script cannot parse are printed in the console.

## What does the script do?
Few simple things. If you add some more, feel free to fork the repository or post a pull request.  
Here is the script's behaviour:

1. Checks the file existence;
2. Parses the file rows and prints out the rows that will be not carried out;
3. Creates the file content and prints it on a file named after the input file.

If the file is named something like `yo_i-am-a-filename.properties` the output file name will be `yoiamafilename.json`.

## Example
A file named example_file.properties with this content:
```
test=super test
another test =    value
thisisthe_last  =    will get  trimmed     
```
will become:
```json
{
    "test": "super test",
    "anothertest": "value",
    "thisisthe_last": "will get  trimmed"
}
```