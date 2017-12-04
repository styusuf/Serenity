import ast
import json
import sys

json_arr = []
with open(sys.argv[1], 'r') as infile:
    for line in infile:
        line = line.lstrip().strip()
        split_line = line.split(" | ")
        if len(split_line) == 1:
            continue
        recipe_id = split_line[0]
        ing_dict = ast.literal_eval(split_line[1])
        info_dict = {}
        info_dict["recipe_id"] = recipe_id
        info_dict["ingredients"] = ing_dict
        json_arr.append(info_dict)

with open(sys.argv[2], 'w') as outfile:
    outfile.write(json.dumps(json_arr, indent=4))