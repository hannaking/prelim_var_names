from types import FunctionType

class RuleRegistry:
    def __init__(self):
        self.registry : dict[str, FunctionType]= {}
    def register(self, name : str):
        def decorator(func : FunctionType):
            self.registry[name] = func
            return func
        return decorator
    def call(self, name : str, *args):
        if name not in self.registry:
            raise KeyError(f'No function called {name}.')
        func = self.registry[name]
        return func(*args)