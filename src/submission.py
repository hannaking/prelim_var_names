from identifier import Identifier
import libcst as cst
from var_finder import VarFinder
from collections import defaultdict
from libcst.metadata import PositionProvider, QualifiedNameProvider
from jorma.src.jorma.static import analyze

class Submission(cst.MetadataDependent):
    METADATA_DEPENDENCIES = (cst.metadata.PositionProvider,cst.metadata.ScopeProvider,cst.metadata.QualifiedNameProvider)

    def __init__(self, filename : str) -> None:
        # read code file
        with open(filename, encoding='utf-8') as f:
            self.file_text: str = f.read()
        # module is the CST
        self.module : cst.Module = cst.parse_module(self.file_text)
        # need wrapper for metadata access
        self.wrapper : cst.MetadataWrapper = cst.MetadataWrapper(self.module)
        self.identifiers : set[cst.CSTNode] = set()
        self.find_identifiers()
    
    def find_identifiers(self) -> None:
        # custom visitor
        finder: VarFinder = VarFinder()
        #position_finder : PositionVisitor = PositionVisitor()
        self.wrapper.visit(finder)
        positions = self.wrapper.resolve(PositionProvider)
        qualified_names = self.wrapper.resolve(QualifiedNameProvider)
        #print(type(qualified_names)) # its a LazyValue
        #print(qualified_names)
        role_dict = analyze(self.file_text)
        #print(len(finder.values))
        names_so_far = []

        for i in range(len(finder.values)):
            node = finder.values[i][2]
            name = node.value
            if name in names_so_far:
                continue
            names_so_far.append(node.value)
            position = positions.get(node)
            parent = finder.values[i][3]
            qualified_name = qualified_names.get(node)
            if isinstance(qualified_name, set):
                #print("qualified_name", qualified_name)
                pass
            else:
                qualified_name = qualified_name()
                #print("qualified_name", qualified_name)
            try:
                qualified_name = next(iter(qualified_name)).name
            except StopIteration:
                with open("../data/skipped_vars.txt", "a") as file:
                    file.write(f'{name} was used but not instantiated. This variable cannot be analyzed and will be skipped.\n')
                #print(f'{name} was used but not instantiated. This variable cannot be analyzed and will be skipped.')
                continue
            if name == qualified_name: #global
                continue
            self.identifiers.add(Identifier(node, position, parent, self.file_text, role_dict, qualified_name))

        #print(names_so_far)
        #print(len(self.identifiers))