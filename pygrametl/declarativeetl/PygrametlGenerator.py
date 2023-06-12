from pygrametl.declarativeetl.parsing import *
import os


class PygramGenerator:
    def __init__(self):
        # TODO: Choose database driver based on DBMS value (psycopg2 for postgres)
        self.db_driver = "psycopg2"
        self.dim_blocks = []
        self.fact_blocks = []
        self.header = (
            "# This file was generated by PygramETL-DeclarativeETL (https://github.com/smath17/declarative-etl)\n\n"
            f"import {self.db_driver}\n"
            "import pygrametl\n"
            "from pygrametl.datasources import SQLSource, CSVSource\n"
            "from pygrametl.tables import CachedDimension, FactTable")

    def __generate_csv_connection(self, csv_file):
        # Example of data source connection
        data_connection = (
            f"data_file_handle = open('{csv_file}', 'r', 16384, \"utf-8\")"
            f"region_source = CSVSource(f=data_file_handle, delimiter=',')"
        )
        return data_connection

    def __open_dw_connection(self, db_name):
        return ("# Open connection to the data warehouse.\n"
                "# CHANGE CONNECTION VALUES TO MATCH YOUR CREDENTIALS\n"
                f"dw_string = \"host='localhost' dbname='{db_name}' user='postgres' password='1234'\"\n"
                f"dw_conn = {self.db_driver}.connect(dw_string)\n"
                "# ConnectionWrapper shares the connection between all relevant PygramETL abstractions\n"
                "# allowing dimensions and fact to connect to their respective tables\n"
                "dw_conn_wrapper = pygrametl.ConnectionWrapper(connection=dw_conn)"
                )

    def __close_dw_connection(self):
        return ("# Commit and close the data warehouse connection\n"
                "dw_conn_wrapper.commit()"
                "dw_conn_wrapper.close()")

    def __generate_dimension(self, dimension: ParsedDimension):
        attribute: ParsedAttribute

        attribute_str = ""
        for attribute in dimension.members:
            attribute_str += f"'{attribute.name}', "

        dim_block = PythonCodeBlock(f"{dimension.name}_Dimension = CachedDimension(", [
            f"name='{dimension.name}_Dimension',",
            f"key='{dimension.key}',",
            f"attributes=[{attribute_str[:-2]}])"])

        # TODO: Consider returning instead
        self.dim_blocks.append(dim_block)

        if dimension.roles is not None:
            self.dim_blocks.append("# Dimension roles")
            for role in dimension.roles:
                self.dim_blocks.append(f"{role}_Dimension = {dimension.name}_Dimension")
            self.dim_blocks.append("")

    def __generate_fact_table(self, fact_table: ParsedFactTable):
        keyref_string = ", ".join(f"'{reference}'" for name, reference in fact_table.list_dim_name_and__reference)
        measure_list = []
        for measure in fact_table.members:
            measure_list.append(f"'{measure.name}'")
        measure_names = ", ".join(measure_list)
        fact_block = PythonCodeBlock(f"{fact_table.name}_Fact_Table = FactTable(", [
            f"name='{fact_table.name}_Fact_Table',",
            f"keyrefs=[{keyref_string}],",
            f"measures=[{measure_names}])"
        ])

        # TODO: Consider returning instead
        self.fact_blocks.append(fact_block)

    def __generate_group(self, group: ParsedGroup):
        for dim in group.dimensions:
            self.__generate_dimension(dim)

        for fact in group.fact_tables:
            self.__generate_fact_table(fact)

    def create_pygrametl_file(self, specification: IntermediateSpecification):
        for dim in specification.dimensions:
            self.__generate_dimension(dim)
        for fact_table in specification.fact_tables:
            self.__generate_fact_table(fact_table)
        if specification.parsed_groups:
            for group in specification.parsed_groups:
                self.__generate_group(group)

        # TODO: Change for better output dir
        working_dir = os.getcwd()
        output_file = open(working_dir + "/PygramETL-generated-setup.py", 'w')
        output_file.write(self.header + "\n\n")
        output_file.write(self.__open_dw_connection(specification.dw_name) + "\n\n")
        for block in self.dim_blocks:
            output_file.write(str(block) + "\n")
        for block in self.fact_blocks:
            output_file.write(str(block))
        output_file.close()


class PythonCodeBlock:
    def __init__(self, head, block):
        self.head = head
        self.block = block

    def __str__(self, indent=""):
        result = indent + self.head + "\n"
        indent += "    "
        for block in self.block:
            if isinstance(block, PythonCodeBlock):
                result += block.__str__(indent)
            else:
                result += indent + block + "\n"
        return result