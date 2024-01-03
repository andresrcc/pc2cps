import argparse
import re


def parse_lines(regular_expression, lines, separator):
    dict_of_values = {}
    for line in lines:
        if separator not in line:
            continue
        split_lines = re.split(regular_expression, line)
        if len(split_lines) == 0:
            continue
        if len(split_lines) > 1:
            dict_of_values[split_lines[0]] = split_lines[1:]
        else:
            dict_of_values[split_lines[0]] = [""]
    return dict_of_values


parser = argparse.ArgumentParser()
parser.add_argument("pc_file")
args = parser.parse_args()
print(args.pc_file)

#TODO handle file not existing
pc_file_handle = open(args.pc_file, 'r')
pc_file_lines = pc_file_handle.readlines()

#parse variables
variable_separator = "="
variable_regex  = f"\s*[,{variable_separator} ]\s*"
pc_variables = parse_lines(variable_regex, pc_file_lines, variable_separator)

#parse attributes
attribute_separator = ":"
attribute_regex = f"\s*[,{variable_separator} ]\s*"
pc_attributes = parse_lines(f"\s*[,{attribute_separator} ]\s*", pc_file_lines, attribute_separator)


print(pc_variables)
print(pc_attributes)

def substitute_pc_variables(pc_variables, pc_attributes):
    for key, value in pc_variables.items():
        for other_key, other_value in pc_attributes.items():
            other_value_string = ' '.join(other_value)
            value_string = ''.join(value)
            if re.search("\s*\${" + key + "}\s*", other_value_string):
                pc_attributes[other_key] = re.sub("\s*\${" + key + "}\s*",value_string.strip(), other_value_string.strip()) 


substitute_pc_variables(pc_variables, pc_variables)
substitute_pc_variables(pc_variables, pc_attributes)
print(pc_attributes)

#TODO how do we provide platform?

cps_file = {
    "Name": pc_attributes["Name"] if "Name" in pc_attributes.keys() else "",
    "Description": pc_attributes["Description"] if "Name" in pc_attributes.keys() else "",
    "Version": pc_attributes["Version"] if "Name" in pc_attributes.keys() else "",
    "Cps-Version": "0.8.1", #TODO pass in as arg?
    "Configurations": [
        "release",
        "debug"
    ],
    "Platform": {},
    "Default-Components": {},
    "Components" : {}, #TODO: Put includes inside here.
    "Requires": {

    } #TODO: Put LIBS here.
}
