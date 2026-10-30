import pytest
import sys
from pathlib import Path
#from ..src.rules import *
rules_path = Path('C://Users//hgkin//Documents//Prelim//prelim_var_names//src')
sys.path.append(str(rules_path))
print(sys.path)
from rules import * 
sys.path.pop()

# ---------------------------
# Helper
# ---------------------------
# baby stand in for Identifier class
class FakeIdentifier:
    def __init__(self, value, types):
        self.value = value
        self.types = types


# ---------------------------
# same_as_type tests
# ---------------------------
# check case sensitivity
# check user-defined types
# check python types
# check it doesn't trigger on substrings
def test_same_as_type_case_mismatch():
    i = FakeIdentifier("present", ["Present"])
    j = FakeIdentifier("Bool", ["bool"])
    print('here')
    assert same_as_type(i) is None
    assert same_as_type(j) is None

def test_same_as_type_case_match():
    i = FakeIdentifier("Present", ["Present"])
    j = FakeIdentifier("int", ["int"])
    assert same_as_type(i) is not None
    assert same_as_type(j) is not None

def test_same_as_type_substring():
    i = FakeIdentifier("string", ["str"])
    assert same_as_type(i) is None


# ---------------------------
# type_in_name tests
# ---------------------------
# check it doesn't trigger on exact matches
# check user-defined types
# check python types
# check case sensitivity
def test_type_in_name_exact_match():
    i = FakeIdentifier("int", ["int"])
    assert type_in_name(i) is None

def test_type_in_name_case_mismatch():
    i = FakeIdentifier("new_present", ["Present"])
    j = FakeIdentifier("is_Bool", ["bool"])
    assert type_in_name(i) is None
    assert type_in_name(j) is None

def test_type_in_name_case_match():
    i = FakeIdentifier("new_Present", ["Present"])
    j = FakeIdentifier("int_for_counting", ["int"])
    assert type_in_name(i) is not None
    assert type_in_name(j) is not None


# ---------------------------
# plural_for_collections tests
# ---------------------------
# types of collections, each with a plural and nonplural
def plural_for_collections_test():
    collections = ['list', 'set', 'frozenset', 'dict', 'tuple', 'range', 'bytearray']
    for collection_type in collections:
        i = FakeIdentifier("values", [collection_type])
        j = FakeIdentifier("value", [collection_type])
        assert plural_for_collections(i) is None
        assert plural_for_collections(j) is not None

# FIXED: will not catch things like 'gifts2'
# because the numeric suffix is not seperated from the word by an _,
# so the word gifts cannot be identified.
def plural_for_collections_numeric_problem():
    i = FakeIdentifier("gifts2", ["list"])
    j = FakeIdentifier("gift2", ["set"])
    assert plural_for_collections(i) is None
    assert plural_for_collections(j) is not None

# ---------------------------
# singular_non_collections tests
# ---------------------------
# types of collections, each with a plural and nonplural
def singular_non_collections_test():
    collections = ['list', 'set', 'frozenset', 'dict', 'tuple', 'range', 'bytearray']
    for collection_type in collections:
        i = FakeIdentifier("values", [collection_type])
        j = FakeIdentifier("value", [collection_type])
        assert singular_non_collections(i) is not None
        assert singular_non_collections(j) is None


# ---------------------------
# boolean_prefix_present tests
# ---------------------------
# check catches each of the suggested prefixes
# check does not trigger on non-boolean variables
# check correctly triggers on non-snake-case
# prefixes: ['is', 'has', 'can', 'should', 'did', 'was']
def test_boolean_prefix_no_prefix():
    i = FakeIdentifier("flag_enabled", ["bool"])
    assert boolean_prefix_present(i) is not None

def test_boolean_prefix_prefixes():
    prefixes = ['is', 'has', 'can', 'should', 'did', 'was']
    for prefix in prefixes:
        i = FakeIdentifier(prefix+"_enabled", ["bool"])
        assert boolean_prefix_present(i) is None

def test_boolean_prefix_not_snake():
    i = FakeIdentifier("hasHat", ["bool"])
    assert boolean_prefix_present(i) is not None


# ---------------------------
# numeric_suffix tests
# ---------------------------
# has numeric suffix
# doesn't have numeric suffix
def test_numeric_suffix_has():
    i = FakeIdentifier("value2", ["double"])
    j = FakeIdentifier("test_case_11", ["list"])
    assert numeric_suffix(i) is not None
    assert numeric_suffix(j) is not None

def test_numeric_suffix_absent():
    i = FakeIdentifier("value", ["double"])
    j = FakeIdentifier("test_case_eleven", ["list"])
    assert numeric_suffix(i) is None
    assert numeric_suffix(j) is None