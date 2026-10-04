from identifier import Identifier
import libcst as cst
from var_finder import VarFinder
from collections import defaultdict
from libcst.metadata import PositionProvider
from jorma.src.jorma.static import analyze

class Submission(cst.MetadataDependent):
    METADATA_DEPENDENCIES = (cst.metadata.PositionProvider,cst.metadata.ScopeProvider)

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

        role_dict = analyze(self.file_text)

        for i in range(len(finder.values)):
            node = finder.values[i][2]
            position = positions.get(node)
            parent = finder.values[i][3]
            self.identifiers.add(Identifier(node, position, parent, self.file_text, role_dict))                