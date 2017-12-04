import json
d = {}
with open('units.txt') as f:
    for line in f.readlines():
        line = line.replace('\n', '')
        vals = line.split('|')
        d[int(vals[0].strip())] = vals[1].strip()

with open('units.js', "w") as f:
    f.write(json.dumps(d))
