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
        default_settings: dict = specification["Default"]
        self.dbms = default_settings.get("DBMS")
        self.pk_name = default_settings.get("pk_naming")
        self.schema_type = default_settings.get("schema_type")
        self.dimension_attribute_type = default_settings.get("dimension_attribute_type")
        self.measure_type = default_settings.get("fact_measure_type")
        self.data_source = default_settings.get("data_source")

        # Extract all dimensions
        all_dimensions = list(specification["dimension"].items())
        parsed_dimensions = self.__parse_dimensions(all_dimensions)

        # Extract all fact tables
        all_fact_tables = list(specification.get("fact").items())
        parsed_fact_tables = self.__parse_fact_tables(all_fact_tables, parsed_dimensions)

        self.dimensions: list[ParsedDimension] = parsed_dimensions
        self.fact_tables: list[ParsedFactTable] = parsed_fact_tables

    def __parse_dimensions(self, dimensions: list):
        """

        @param dimensions: List of dimensions from specification
        @return: List of ParsedDimension
        """
        parsed_dimensions = []
        # For each dimension parse it and append to specification
        for dimension in dimensions:
            # dimension = ('table name', {{'attributes': 'name, age, sex'}, {'roles': 'age'}})
            dim_name, dim_content = dimension
            dim_attributes = dim_content.get("attributes", )
            dim_roles = dim_content.get("roles")
            parsed_dimensions.append(ParsedDimension(dim_name, dim_attributes, dim_roles, dim_name + self.pk_name,
                                                     self.dimension_attribute_type))

        return parsed_dimensions

    def __parse_fact_tables(self, fact_tables: list, parsed_dimensions: list):
        """

        @param fact_tables: List of fact tables from specification
        @param parsed_dimensions: List of parsed dimensions related to the fact tables
        @return: List of ParsedFactTable
        """
        parsed_fact_tables = []

        for fact_table in fact_tables:
            name = fact_table[0]
            measures = fact_table[1].get("measures")
            # TODO: Do not take every dimension as key_ref
            table_refs = []
            for dimension in parsed_dimensions:
                table_refs.append(dimension.name)
            parsed_fact_tables.append(ParsedFactTable(name, measures, self.measure_type, table_refs))

        return parsed_fact_tables


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
    keys: list[str]

    def __init__(self, name, members: list[ParsedAttribute], keys, default_type):
        self.name = name
        self.members = members
        # 1 key for primary, more for foreign
        self.keys = keys
        self.default_type = default_type


class ParsedDimension(ParsedTable):
    name: str
    roles: list[str]

    def __init__(self, name, attributes, roles, key, default_type):
        members = ParsedAttribute.from_list(attributes, default_type)
        super().__init__(name, members, [key], default_type)
        self.roles = roles


class ParsedFactTable(ParsedTable):
    name: str

    def __init__(self, name, measures, default_type, key_refs):
        members = ParsedAttribute.from_list(measures, default_type)
        super().__init__(name, members, key_refs, default_type)
