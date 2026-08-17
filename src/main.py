from submission import Submission
import runpy                          # how to improve?
from namesake.namesake import *

filename = 'sample.py'
entry = Submission(filename)

result = runpy.run_path('rules.py')
registry = result["registry"]

run_namesake([i.value for i in entry.identifiers])

for i in entry.identifiers:
    # run the rules from the registry
    for key in registry.registry:
        registry.call(key, i)