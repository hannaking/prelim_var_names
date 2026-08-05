import libcst as cst
import jedi
from libcst.metadata import CodeRange

class Identifier(cst.MetadataDependent):
    METADATA_DEPENDENCIES = (cst.metadata.PositionProvider,)

    def __init__(self, node : cst.Node, position : cst.CodeRange, source_code : str): # start : cst.CodePosition, end : cst.CodePosition, source_code : str) -> None:
        self.value : str = node.value
        self.range : cst.metadata.CodeRange = cst.metadata.CodeRange(position.start, position.end)

        # Jedi Script object for type inference - also why i need the position info
        self.script = jedi.Script(source_code)
        self.types : list[str] = self.type_with_jedi(node)
        # do I also need parent? ex. assign, attribute, for, etc
        self.plural : bool = self.plurality()

    def type_with_jedi(self, node : cst.Node) -> list[str]:
        try:
            # Jedi expects 1-based line/column numbers
            # code range object is 1-indexed for lines and 0-indexed for columns
            inferred = self.script.infer(line=self.range.start.line, column=self.range.start.column)
            if inferred:
                # may result in more than one type for a single variable
                types = {inf.name for inf in inferred}
                return types
            else:
                return ["unknown"]
        except Exception as e:
            print(f"Problem inferring type for '{node.value}': {e}")

    def assign_role(self) -> None:
        pass

    def plurality(self) -> bool:
        pass