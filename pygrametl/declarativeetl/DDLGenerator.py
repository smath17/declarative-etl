import os

from pygrametl.declarativeetl.parsing import *


# noinspection SqlDialectInspection,SqlNoDataSourceInspection
class CreateTableStatement:
    def __init__(self, table: ParsedTable, key_type: str):
        # Add descriptive name
        if isinstance(table, ParsedDimension):
            self.name = table.name + "_Dimension"
        elif isinstance(table, ParsedFactTable):
            self.name = table.name + "_Fact_Table"

        # Format members as strings separated by commas and lines
        str_columns = [str(member) for member in table.members]
        self.columns_format = ",\n".join(str_columns)

        # TODO: Consider changing keys for fkeys and pkeys
        # TODO: fix this shit
        if key_type == "FOREIGN KEY":
            keys = ["{0}FK INT REFERENCES {1}".format(key, key + "_Dimension") for key in table.keys]
        else:
            keys = ["{0} INT {1}".format(key, key_type) for key in table.keys]
        self.keys_format = ",\n".join(keys) + ","


    def __str__(self):
        return """CREATE TABLE {name}
(
{keys}
{columns}
);""".format(name=self.name, columns=self.columns_format, keys=self.keys_format)


class CreateDimension(CreateTableStatement):
    def __init__(self, table):
        # TODO: should be able to have foreign keys, for snowflake
        super().__init__(table, key_type="PRIMARY KEY")


class CreateFactTable(CreateTableStatement):
    def __init__(self, table):
        # TODO: Should also have primary composite key
        super().__init__(table, key_type="FOREIGN KEY")


class DDLGenerator:
    def __init__(self, specification: IntermediateSpecification):
        self.spec = specification

    def create_group_statements(self, group: ParsedGroup):
        dim_statements = []
        fact_statements = []

        for dim in group.dimensions:
            dim_statements.append(CreateDimension(dim))
        for fact in group.fact_tables:
            fact_statements.append(CreateFactTable(fact))

        return dim_statements, fact_statements

    def make_ddl_file(self):
        dim_statements = []
        fact_statements = []
        for dim in self.spec.dimensions:
            dim_statements.append(CreateDimension(dim))
        for fact in self.spec.fact_tables:
            fact_statements.append(CreateFactTable(fact))
        if self.spec.parsed_groups:
            for group in self.spec.parsed_groups:
                dim_stmts, fact_stmts = self.create_group_statements(group)
                dim_statements.extend(dim_stmts)
                fact_statements.extend(fact_stmts)

        working_dir = os.getcwd()
        file = open(working_dir + "\\out/DDL-generated-setup.ddl", 'w')
        for statement in dim_statements:
            file.write(str(statement) + "\n\n")
        for statement in fact_statements:
            file.write(str(statement) + "\n\n")


# noinspection SqlDialectInspection,SqlNoDataSourceInspection
class CreateDatabaseStatement:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return """CREATE DATABASE {name};""".format(name=self.name)
