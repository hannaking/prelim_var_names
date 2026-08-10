from submission import Submission
from registry import RULES
from identifier import Identifier

filename = 'sample.py'
entry = Submission(filename)

for i in entry.identifiers:
    # run the rules from the registry
    for key in RULES:                     # how to improve?
        print(f'running {key}')
        RULES[key](i)