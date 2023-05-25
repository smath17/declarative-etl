import tomllib


class IntermediateSpecification:
    """A class for accessing structured specification from TOML file """

    def __init__(self, file_path):
        """
        Creates an IntermediateSpecification object from a TOML file.

        @param file_path: Path to TOML file
        """
        with open(file_path, mode="rb") as toml_specification:
            specification = tomllib.load(toml_specification)

        # Read and load default settings from file
        default_settings = specification["Default"]
        self.dbms = default_settings["DBMS"]
        self.pk_name = default_settings["pk_naming"]
        self.schema_type = default_settings["schema_type"]
        self.dimension_attribute_type = default_settings["dimension_attribute_type"]
        self.measure_type = default_settings["fact_measure_type"]

        # Extract all dimensions
        all_dimensions = list(specification["dimension"].items())
        parsed_dimensions = []
        # For each dimension parse it and append to specification
        for dimension in all_dimensions:
            # dimension = ('table name', {'attributes': 'name, age, sex'}, 'roles': {'age'}})
            dim_name, dim_content = dimension
            dim_attributes = dim_content["attributes"]
            dim_roles = None
            if 'roles' in dim_content:
                dim_roles = dim_content["roles"]
            parsed_dimensions.append(ParsedDimension(dim_name, dim_attributes, dim_roles, dim_name + self.pk_name,
                                                     self.dimension_attribute_type))

        # Extract all fact tables
        all_fact_tables = list(specification["fact"].items())
        parsed_fact_tables = []
        for fact_table in all_fact_tables:
            fact_table_name, fact_table_content = fact_table
            fact_table_measures = fact_table_content["measures"]
            # TODO: Do not take every dimension as key_ref
            key_refs = [dimension.key for dimension in parsed_dimensions]
            parsed_fact_tables.append(
                ParsedFactTable(fact_table_name, fact_table_measures, self.measure_type, key_refs))

        self.dimensions: list[ParsedDimension] = parsed_dimensions
        self.fact_tables: list[ParsedFactTable] = parsed_fact_tables


class ParsedAttribute:
    name: str
    attribute_type: str

    def __init__(self, name, attribute_type):
        self.name = name
        self.type = attribute_type

    @classmethod
    def from_list(cls, attribute_list: list[str], default_type):
        result = []
        for attribute in attribute_list:
            if ':' in attribute:
                attribute_type: str
                attribute_name, attribute_type = attribute.split(':', 1)
                result.append(cls(attribute_name, attribute_type.strip()))
            else:
                result.append(cls(attribute, default_type))
        return result

    def __str__(self):
        return f"{self.name} {self.type}"


class ParsedTable:
    def __init__(self, name, members: list[ParsedAttribute], keys, default_type):
        self.name = name
        self.members = members
        # 1 key for primary, more for foreign
        self.keys = keys
        self.default_type = default_type


class ParsedDimension(ParsedTable):
    name: str
    attributes: list[ParsedAttribute]
    roles: list[str]

    def __init__(self, name, attributes, roles, key, default_type):
        members = ParsedAttribute.from_list(attributes)
        super().__init__(name, members, list(key), default_type)
        self.roles = roles


class ParsedFactTable(ParsedTable):
    name: str
    measures: list[ParsedAttribute]

    def __init__(self, name, measures, default_type, key_refs):
        members = ParsedAttribute.from_list(measures, default_type)
        super().__init__(name, members, key_refs, default_type)
