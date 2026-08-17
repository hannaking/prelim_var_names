from dataclasses import dataclass 

@dataclass
class Present:
    weight: float
    for_you: bool
    giver: str
    color: str

def giver_of_my_smallest_present(Presents: list[Present])->str:
    test = 9999999999999999999999999999999999999.9999999999999999
    smallest_present = "nothing"
    for p in Presents:
        if p.for_you == True:
            if p.weight < test:
                test = p.weight
                smallest_present = p.giver
    return smallest_present