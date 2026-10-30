from identifier import Identifier
from registry import *
import constants as constants
from registry import RuleRegistry
import nltk
#https://pythonguides.com/remove-numbers-from-strings-in-python/
import re
#from pep8_naming.pep8ext_naming import global_variable_check, class_variable_check, function_variable_check
#nltk.download('punkt')
#nltk.download('punkt_tab')
#nltk.download('averaged_perceptron_tagger')

with open("../data/count_1w100k.txt", "r") as file:
    dictionary = [line.split()[0].strip().lower() for line in file if line.strip()]
with open("../data/metasyntactic.txt", "r") as file:
    metasyntactic = [line.strip() for line in file]
registry = RuleRegistry()

def so_far_most_wanted(i:Identifier):
    name = i.value
    if i.role == "MOST_WANTED" and "so_far" not in name:
        return f'You may want to incorporate "so far" into your variable {name}, as you are repeatedly updating it to the most wanted so far.'
    return None

@registry.register("banned single letter names")
def pep_eight_banned_single(i:Identifier):
    name = i.value
    if name in constants.PEP8_BANNED_SINGLE_CHARACTER:
        return f'PEP8, the Python style guide, forbids the use of l, O, and I as single-letter variable names because they are easily confused for other characters. Your variable {name} uses one of these.'
    return None

@registry.register("snake case")
def enforce_snake_case(i : Identifier):
    name = i.value
    if any(char.isupper() for char in name): 
        return f'Python\'s snake_case requires all characters in a variable name to be lowercase. Your variable {name} contains a capital letter. This may have happened if you were using camelCase instead.'
    digit = get_digit_index(name)
    if digit is not None and name[digit-1] != '_':
        return f'In order to conform to the snake_case convention, please seperate words and numbers with an _. Your variable {name} is missing this.'
    return None

# helper
def get_digit_index(name : str):
    indices = [i for i, char in enumerate(name) if char.isdigit()]
    if len(indices) > 0:
        return indices[0]
    return None

@registry.register("avoid single letter names")
def avoid_single_letter(i : Identifier):
    name = i.value
    role = i.role
    if len(name) == 1 and name not in constants.EXCEPTED_SINGLE_LETTER and role == "STEPPER":
        return f'Avoid single letter variable names. You have used {name}.'
    return None

@registry.register("same as type")
def same_as_type(i : Identifier):
    name = i.value
    if name == i.types[0]:
        return f'Do not use the type, {i.types[0]}, as the name for {name}.'
    return None

@registry.register("type in name")
def type_in_name(i : Identifier):
    name = i.value
    if i.types[0] in name and same_as_type(i) is None:
        return f'Do not use the type, {i.types[0]}, in the name for {name}.'
    return None

@registry.register("plural for collections")
def plural_for_collections(i : Identifier):
    name = i.value
    cleaned_name = re.sub(r'\d+', '', name)

    if i.types[0] in constants.COLLECTION_TYPES and not is_plural(cleaned_name):
        return f'Your variable {name} is a collection type {i.types[0]}, but {name} is singular. Collection type variables may hold multiple values and should therefore be plural.'
    return None

@registry.register("singular for noncollections")
def singular_non_collections(i : Identifier):
    name = i.value
    if i.types[0] not in constants.COLLECTION_TYPES and is_plural(name):
        return f'Your variable {name} is a singular type {i.types[0]}, but {name} is plural. Non-collection type variables hold only one value at a time and should therefore be singular.'
    return None

def is_plural(name : str) -> bool:
    tokens = nltk.word_tokenize(name)
    tagged = nltk.pos_tag(tokens) # gives me list of tuples of (word, tag)
    tags = [t[1] for t in tagged]
    return 'NNS' in tags

@registry.register("boolean prefix")
def boolean_prefix_present(i : Identifier):
    name = i.value
    words : list[str] = name.split('_')
    if i.types[0] == "bool" and words[0] not in constants.BOOLEAN_PREFIX:
        return f'Your boolean variable {name} should include a verb prefix. Example prefixes include is, was, should, can, did, and had.'
    return None

@registry.register("numeric suffix")
def numeric_suffix(i : Identifier):
    name = i.value
    if name[-1].isdigit():
        return f'Your variable {name} is differentiated by a number at the end of the variable name. This can be confusing; consider renaming.'
    return None

# https://pythonguides.com/remove-numbers-from-strings-in-python/
@registry.register("dictionary words")
def use_dictionary_words(i : Identifier):
    name = i.value
    name = re.sub(r'\d+','', name)
    split = name.split('_')
    for word in split:
        if word.lower() not in dictionary:
            return f'Your variable {name} may contain an uncommon, misspelled, or abbreviated word {word}. Consider using English dictionary word(s) instead.'
    return None

@registry.register("metasyntactic")
def uses_metasyntactic_name(i : Identifier):
    name = i.value
    if name.lower() in metasyntactic:
        return f'Use meaningful names. {name} is a placeholder name.'
    return None

@registry.register("number word name")
def number_word_name(i : Identifier):
    name = i.value
    for target in constants.NUMERIC_NAMES:
        if name in target:
            return f'Your variable {name} uses a numeric name, {target}. Consider changing this variable name.'
    return None