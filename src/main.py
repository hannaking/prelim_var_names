from submission import Submission
from pathlib import Path
import libcst
from registry import RuleRegistry
#import subprocess
#import sys

EXCEPTED_VAR_NAMES = ["for_you"]

def run(filename : Path, registry : RuleRegistry):
    alias = Path(filename).stem

    try:
        entry = Submission(filename)
    except libcst._exceptions.ParserSyntaxError:
        with open("../data/syntax_errors.txt", "a") as file:
            file.write(f'{alias}; syntax error\n')
        return
    #print("here")
    # run pep8 naming checks first
    #  if any trigger, don't run the registry on that var name
    #ruff_result = subprocess.run([sys.executable,
    #                              "-m",
    #                              "ruff",
    #                              "check",
    #                              filename,
    #                              "--select",
    #                              "N,PL",
    #                              "--output-format",
    #                              "json"],
    #                              capture_output=True,
    #                              text=True)
    #print(f'ruff stdout: {ruff_result.stdout}')

    output : str = ""
    for i in entry.identifiers:
        # run the rules from the registry
        if i.value in EXCEPTED_VAR_NAMES:
            with open("../data/skipped_vars.txt", "a") as file:
                file.write(f'{i.value} was provided by the assignment and will be skipped.\n')
            continue
        for key in registry.registry:
            text_from_rule : str = registry.call(key, i)
            if text_from_rule is not None:
                output += (f'{alias}; {i.qualified_name}; {i.types[0]}; {key}; {True}\n')# {text_from_rule}\n')
            else:
                output += (f'{alias}; {i.qualified_name}; {i.types[0]}; {key}; {False}\n')

    # diagnosis, rule ID, and identifier in to a full-report file
    with open("../data/full_report.txt", "a") as file:
        file.write(output)
    return