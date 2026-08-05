from submission import Submission
import constants

filename = 'sample.py'
entry = Submission(filename)

for i in entry.identifiers:
    name = i.value
    # Rule: avoid single letter names - except i, j, x, y, z
    if len(name) == 1 and name not in constants.EXCEPTED_SINGLE_LETTER:
        print(f'Avoid single letter variable names. You have used {name}.')
    # Rule: lowercase
    if name != name.lower():
        print(f'{name} violates the snake_case capitalization convention.')
    # Rule: do not use same name as type
    if name in i.types:
        print(f'Do not use the type, {i.types}, as the name for {name}.')