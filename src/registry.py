from types import FunctionType

RULES : dict[str, FunctionType]= {}

def register_rule(name : str):
    def decorator(func : FunctionType):
        RULES[name] = func
        return func
    return decorator