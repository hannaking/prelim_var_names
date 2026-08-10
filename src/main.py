from submission import Submission
import runpy

filename = 'sample.py'
entry = Submission(filename)

result = runpy.run_path('rules.py')
registry = result["registry"]

for i in entry.identifiers:
    # run the rules from the registry
    for key in registry.registry:
        registry.call(key, i)