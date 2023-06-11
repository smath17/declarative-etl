from pygrametl.declarativeetl.DDLGenerator import DDLGenerator
from pygrametl.declarativeetl.PygramGenerator import PygramGenerator
from pygrametl.declarativeetl.parsing import IntermediateSpecification


def create_source_files(spec_filepath):
    spec = IntermediateSpecification(spec_filepath)
    _generate_pygram(spec)
    _generate_ddl(spec)


def _generate_pygram(spec):
    generator = PygramGenerator()
    generator.create_pygram_file(spec)


def _generate_ddl(spec):
    ddl_generator = DDLGenerator(spec)
    ddl_generator.make_ddl_file()
