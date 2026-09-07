from dataclasses import dataclass 

@dataclass
class Present:
    weight: float
    for_you: bool
    giver: str
    color: str

present : Present = Present()
output_str : str = "test string"
lis = []
output_string : str = "test"
numbers : int = 6
number : int = 1
names : list[str] = ["Anthony", "Benedict", "C", "Daphne", "Eloise", "Francesca", "Gregory", "Hyacinth"]
active : bool = True
is_open = False