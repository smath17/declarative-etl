from pygrametl.declarativeetl.DDLGenerator import DDLGenerator
from pygrametl.declarativeetl.PygrametlGenerator import PygramGenerator
from pygrametl.declarativeetl.parsing import IntermediateSpecification


def create_source_files(spec_filepath):
    spec = IntermediateSpecification(spec_filepath)
    _generate_pygrametl(spec)
    _generate_ddl(spec)


def _generate_pygrametl(spec):
    generator = PygramGenerator()
    generator.create_pygrametl_file(spec)


def _generate_ddl(spec):
    ddl_generator = DDLGenerator(spec)
    ddl_generator.make_ddl_file()
