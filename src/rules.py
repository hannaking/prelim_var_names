from identifier import Identifier
from registry import *
import constants
from registry import RuleRegistry
import nltk
#nltk.download('punkt')
#nltk.download('punkt_tab')
#nltk.download('averaged_perceptron_tagger')

with open("../data/count_1w100k.txt", "r") as file:
    dictionary = [line.split()[0].strip().lower() for line in file if line.strip()]
with open("../data/metasyntactic.txt", "r") as file:
    metasyntactic = [line.strip() for line in file]
registry = RuleRegistry()

#@registry.register("avoid single letter names")
#def avoid_single_letter(i : Identifier):
#    name = i.value
#    if len(name) == 1 and name not in constants.EXCEPTED_SINGLE_LETTER:
#            print(f'Avoid single letter variable names. You have used {name}.')

#@registry.register("lowercase")
#def lowercase(i : Identifier):
#    name = i.value
#    if name != name.lower():
#        print(f'{name} violates the snake_case capitalization convention.')

@registry.register("same as type")
def same_as_type(i : Identifier):
    name = i.value
    if name.lower() == i.types[0].lower():
        print(f'Do not use the type, {i.types[0]}, as the name for {name}.')

@registry.register("type in name")
def type_in_name(i : Identifier):
    name = i.value
    if i.types[0].lower() in name.lower():
        print(f'Do not use the type, {i.types[0]}, as the name for {name}.')

@registry.register("plural for collections")
def plural_for_collections(i : Identifier):
    name = i.value
    if i.types[0] in constants.COLLECTION_TYPES and not is_plural(name):
        print(f'Your variable {name} is a collection type {i.types[0]}, but {name} is singular. Collection type variables may hold multiple values and should therefore be plural.')

@registry.register("singular for noncollections")
def singluar_non_collections(i : Identifier):
    name = i.value
    if i.types[0] not in constants.COLLECTION_TYPES and is_plural(name):
        print(f'Your variable {name} is a singular type {i.types[0]}, but {name} is plural. Non-collection type variables hold only one value at a time and should therefore be singular.')

def is_plural(name : str) -> bool:
    tokens = nltk.word_tokenize(name)
    tagged = nltk.pos_tag(tokens) # gives me list of tuples of (word, tag)
    tags = [t[1] for t in tagged]
    return 'NNS' in tags

@registry.register("boolean_prefix")
def boolean_prefix_present(i : Identifier):
    name = i.value
    words : list[str] = name.split('_')
    if i.types[0] == bool and words[0] not in constants.BOOLEAN_PREFIX:
        print(f'Your boolean variable {name} should include a verb prefix. Example prefixes include is, was, should, can, did, and had.')

#@registry.register("dictionary_words")
#def use_dictionary_words(i : Identifier):
#    name = i.value
#    split = name.split('_')
#    for word in split:
#        if word.lower() not in dictionary:
#            print(f'Your variable {name} may contain an uncommon word {word}. Consider using English dictionary word(s) instead.')

#@registry.register("metasyntactic")
#def uses_metasyntactic_name(i : Identifier):
#    name = i.value
#    if name.lower() in metasyntactic:
#        print(f'Use meaningful names. {name} is a placeholder name.')
