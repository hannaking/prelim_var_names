from submission import Submission
import runpy                          # how to improve?
from namesake.namesake import *

filename = '../data/sample.py'
entry = Submission(filename)

result = runpy.run_path('rules.py')

#exec(open("rules.py").read()) # doesn't seem particularly faster than runpy? suggestions?

registry = result["registry"]

#run_namesake([i.value for i in entry.identifiers])
#print()
output : str = ""
for i in entry.identifiers:
    # run the rules from the registry
    for key in registry.registry:
        text_from_rule : str = registry.call(key, i)
        if text_from_rule is not None:
            output += (f'Name misaligned with type; {key}; {text_from_rule}\n')


# diagnosis, rule, identifier into a text file (seperated by ;)
with open('../data/report.txt', 'w') as file:
    file.write(output)