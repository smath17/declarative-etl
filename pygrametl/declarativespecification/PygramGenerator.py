from pygrametl.declarativespecification.parsing import *
import os


class PygramGenerator:
    def __init__(self, specification: IntermediateSpecification):
        self.dimblocks = []
        self.factblocks = []
        self.keys = []
        for dimension in specification.dimensions:
            self.keys.append(f"'{dimension.name}{specification.pk_name}'")

    def generate_dimension(self, dimension: ParsedDimension):
        attribute_str = ""
        attribute: ParsedAttribute
        for attribute in dimension.attributes:
            attribute_str += f"'{attribute.name}' "

        dimblock = CodeBlock(f"{dimension.name}dim = CachedDimension(", [
            f"name='{dimension.name}',",
            f"key='{dimension.key}',",
            f"attributes=[{attribute_str.strip()}])"])

        # TODO: Consider returning instead
        self.dimblocks.append(dimblock)

    def generate_fact_table(self, fact_table: ParsedFactTable):
        keyref_string = ", ".join(self.keys)
        measure_list = []
        for measure in fact_table.measures:
            measure_list.append(f"'{measure.name}'")
        measure_names = ", ".join(measure_list)
        factblock = CodeBlock(f"{fact_table.name} = FactTable(", [
            f"name='{fact_table.name}',",
            f"keyrefs=[{keyref_string}],",
            f"measures=[{measure_names}])"
        ])

        # TODO: Consider returning instead
        self.factblocks.append(factblock)

    def create_pygram_file(self):
        # TODO: Change for better output dir
        working_dir = os.getcwd()
        file = open(working_dir + "/Pygram-generated-setup", 'w')
        for block in self.dimblocks:
            file.write(block + "\n\n")
        for block in self.factblocks:
            file.write(block + "\n\n")
        file.close()


class CodeBlock:
    def __init__(self, head, block):
        self.head = head
        self.block = block

    def __str__(self, indent=""):
        result = indent + self.head + ":\n"
        indent += "    "
        for block in self.block:
            if isinstance(block, CodeBlock):
                result += block.__str__(indent)
            else:
                result += indent + block + "\n"
        return result
