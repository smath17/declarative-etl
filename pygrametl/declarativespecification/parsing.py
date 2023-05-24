import tomllib

from pygrametl.tables import FactTable, Dimension


class IntermediateSpecification:
    """A class for accessing structured specification from TOML file """

    def __init__(self, dbms, pk_name, schema_type, dimension_attribute_type, measure_type):
        self.dbms = dbms
        self.pk_name = pk_name
        self.schema_type = schema_type
        self.dimension_attribute_type = dimension_attribute_type
        self.measure_type = measure_type
        self.dimensions = []
        self.fact_tables = []
        # TODO: Exchange dims and facts for groups, probably

    def add_dimension(self, dimension: Dimension):
        # TODO: make use of the different types of dimensions
        self.dimensions.append(dimension)

    def add_fact_table(self, fact_table: FactTable):
        self.fact_table = fact_table

    @classmethod
    def from_file(cls, path):
        """
        Instantiate class from a TOML file
        @param path: Path to TOML file
        @return: IntermediateSpecification object
        """
        with open(path, mode="rb") as file:
            specification = tomllib.load(file)

        # Read and load default settings from file
        default_settings = specification["Default"]
        intermediate_spec = IntermediateSpecification(
            default_settings["DBMS"],
            default_settings["pk_name"],
            default_settings["schema_type"],
            default_settings["dimension_attribute_type"],
            default_settings["measure_type"]
        )
        # TODO: Go through all dimensions and add them
        # This does not work dimension_dict = {k: specification[k] for k in range(1, second_last_dict_index)}
        return intermediate_spec


class ParsedDimension:
    def __init__(self, ):
        pass


class ParsedAttribute:
    def __init__(self, name, attribute_type="default"):
        self.name = name
        self.type = attribute_type
