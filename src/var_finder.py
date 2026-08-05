import libcst as cst
import libcst.matchers as m
from libcst.metadata import ParentNodeProvider #, PositionProvider

# Name nodes present for variables, function names, class names, import aliases, and attribute accesses
# I only want variable and attribute
class VarFinder(cst.CSTVisitor):
    METADATA_DEPENDENCIES = (ParentNodeProvider,)
    def __init__(self) -> None:
        self.variables : set[cst.CSTNode] = set()
        self.values : set[str] = set()
        #self.start_positions = list()
        #self.end_positions = list()

    def visit_Name(self, node: cst.Name) -> None:
        parent = self.get_metadata(ParentNodeProvider, node)
        # filter for variables, loop targets and iterators, and attributes only
        # also exclude nodes with values already present (prevents repeated names in Submission's identifiers)
        if isinstance(parent, (cst.AssignTarget, cst.AnnAssign, cst.Attribute, cst.For)) and node.value not in self.values:
            self.variables.add(node)
            self.values.add(node.value)
            #self.start_positions.append(self.get_metadata(PositionProvider, node).start)
            #self.end_positions.append(self.get_metadata(PositionProvider, node).end)
