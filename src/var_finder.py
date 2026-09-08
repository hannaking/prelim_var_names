import libcst as cst
import libcst.matchers as m
from libcst.metadata import ParentNodeProvider, QualifiedNameProvider #, PositionProvider

# Name nodes present for variables, function names, class names, import aliases, and attribute accesses
# I only want variable and attribute
class VarFinder(cst.CSTVisitor):
    METADATA_DEPENDENCIES = (ParentNodeProvider, QualifiedNameProvider)
    def __init__(self) -> None:
        self.qualifieds = []
        self.values = []
        #self.start_positions = list()
        #self.end_positions = list()

    def visit_Name(self, node: cst.Name) -> None:
        parent = self.get_metadata(ParentNodeProvider, node)
        qualified_name = self.get_metadata(QualifiedNameProvider, node)
        # filter for variables, loop targets and iterators, and attributes only
        # also exclude nodes with values already present (prevents repeated names in Submission's identifiers)
        if isinstance(parent, (cst.AssignTarget, cst.AnnAssign, cst.Attribute, cst.For)) and qualified_name not in self.qualifieds:
            self.qualifieds.append(qualified_name)
            self.values.append((qualified_name, node.value, node, parent))