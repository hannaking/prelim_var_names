import libcst as cst
import jedi
from jorma.src.jorma.varinfo import VarInfo

class Identifier(cst.MetadataDependent):
    METADATA_DEPENDENCIES = (cst.metadata.PositionProvider, cst.metadata.ParentNodeProvider, cst.metadata.QualifiedNameProvider)

    def __init__(self, node : cst.Node, position : cst.CodeRange, parent, source_code : str, role_dict : list[tuple[VarInfo, str]], qualified_name : str):
        self.qualified_name : str = qualified_name
        self.value : str = self.qualified_name.rsplit(".", 1)[-1]
        self.range : cst.metadata.CodeRange = cst.metadata.CodeRange(position.start, position.end)
        self.parent = parent

        # Jedi Script object for type inference - also why i need the position info
        self.script = jedi.Script(source_code)
        self.types : list[str] = self.type_with_jedi(node)
        # do I also need parent? ex. assign, attribute, for, etc
        #self.plural : bool = self.is_plural()
        self.role = self.get_role(self.value, role_dict)

    def type_with_jedi(self, node : cst.Node) -> list[str]:
        try:
            # Jedi expects 1-based line/column numbers
            # code range object is 1-indexed for lines and 0-indexed for columns
            inferred = self.script.infer(line=self.range.start.line, column=self.range.start.column)
            if inferred:
                # may result in more than one type for a single variable
                types = [inf.name for inf in inferred]
                return types
            else:
                return ["unknown"]
        except Exception as e:
            print(f"Problem inferring type for '{node.value}': {e}")

    def is_attribute(self) -> bool:
        #print(type(self.parent))
        return isinstance(self.parent, cst.Attribute)

    def get_role(self, target, role_dict) -> str:
        role = "unknown"
        for item, assignment in role_dict:
            if item.name == target:
                role = assignment
        return role

    def is_plural(self) -> bool:
        pass