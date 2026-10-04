from submission import Submission
import runpy                          # how to improve?
from namesake.namesake import *
import sys
from pathlib import Path
import libcst

filename = sys.argv[1]
# Source - https://stackoverflow.com/a/47496703
# Posted by mxdbld, modified by community. See post 'Timeline' for change history
# Retrieved 2026-10-01, License - CC BY-SA 4.0
alias = Path(filename).stem

print("running on", alias)

try:
    entry = Submission(filename)
except libcst._exceptions.ParserSyntaxError:
    with open("../data/full_report.txt", "a") as file:
        file.write(f'syntax error in {alias}\n')
    sys.exit(0)

#result = subprocess.run(["python", "rules.py"], capture_output=True, check=False).stdout

#print("Result:", result)

result = runpy.run_path('rules.py')

#exec(open("rules.py").read()) # doesn't seem particularly faster than runpy? suggestions?

registry = result["type_registry"]

#run_namesake([i.value for i in entry.identifiers])
#print()
output : str = ""
for i in entry.identifiers:
    #print(i.value, i.role)
    # run the rules from the registry
    for key in registry.registry:
        text_from_rule : str = registry.call(key, i)
        if text_from_rule is not None:
            output += (f'{alias}; Name misaligned with type; {key}; {i.value}\n')# {text_from_rule}\n')

# diagnosis, rule ID, and identifier in to a full-report file
with open("../data/full_report.txt", "a") as file:
    file.write(output)