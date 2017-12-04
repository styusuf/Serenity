import numpy as np
import pdb

data = []
checked = set()
with open("TestData/frequency.txt", 'r') as infile:
    infile.readline()
    infile.readline()
    for line in infile:
        split = line.split('|')
        if len(split) != 3:
            continue
        id_ = str(split[0].lstrip().strip())
        ingred = split[1].strip().replace("'", '')
        data.append([id_, ingred])
data = np.array(data)

groups = []
for idx in range(data.shape[0]):
    print
    print "Checking ingredient #{}".format(idx)
    if data[idx, 0] in checked:
        continue
    checked.add(data[idx, 0])
    new_group = [(data[idx, 0], data[idx, 1])]

    curr_id = data[idx, 0]
    for idx2 in range(idx+1, data.shape[0]):
        response = " "
        new_id = data[idx2, 0]
        if new_id.endswith(curr_id):
            while (response.lower()[0] != "y") and (response.lower()[0] != "n"):
                response = raw_input("Does {} belong in group {}?".format(data[idx2,:], new_group))
                response += " "

        if response.lower()[0] == "y":
            new_group.append([new_id, data[idx2, 1]])

    groups.append(new_group)

with open("Output/groups.txt", 'w') as outfile:
    for group in groups:
        outfile.write( ",".join([x[0] for x in group]))
        outfile.write("\n")
