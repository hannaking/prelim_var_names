from identifier import Identifier
from registry import *
import constants
from registry import RuleRegistry
import nltk
from nltk.corpus import words       # also tried brown, both still flag common words as uncommon/nondictionary

#nltk.download('words')

registry = RuleRegistry()

@registry.register("avoid single letter names")
def avoid_single_letter(i : Identifier):
    name = i.value
    if len(name) == 1 and name not in constants.EXCEPTED_SINGLE_LETTER:
            print(f'Avoid single letter variable names. You have used {name}.')

@registry.register("lowercase")
def lowercase(i : Identifier):
    name = i.value
    if name != name.lower():
        print(f'{name} violates the snake_case capitalization convention.')

@registry.register("same as type")
def same_as_type(i : Identifier):
    name = i.value.lower()
    if name == i.types[0].lower():
        print(f'Do not use the type, {i.types[0]}, as the name for {name}.')

@registry.register("dictionary_words")
def use_dictionary_words(i : Identifier):
    name = i.value
    split = name.split('_')
    for word in split:
        if word not in words.words() and word.lower() not in words.words():
            print(f'Your variable {name} may contain an uncommon word {word}. Consider using English dictionary word(s) instead.')

