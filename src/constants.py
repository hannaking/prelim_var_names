from typing import Final

EXCEPTED_SINGLE_LETTER : Final[str] = ['i', 'j', 'z', 'x', 'y']
PLURAL_TAGS : Final[str] = ["NNS", "NNPS"]

ALL_TYPES : Final[str] = ['bool', 'int', 'float', 'complex', 'list', 'tuple', 'range', 'str', 'Template', 'bytes', 'bytearray', 'memoryview', 'set', 'frozenset', 'dict', 'NoneType', 'Ellipsis', 'NotImplemented']
COLLECTION_TYPES : Final[str] = ['list', 'set', 'frozenset', 'dict', 'tuple', 'range', 'bytearray']

BOOLEAN_PREFIX : Final[str] = ['is', 'has', 'can', 'should', 'did', 'was']