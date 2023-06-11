import sys

from pygrametl.declarativeetl.DDLGenerator import DDLGenerator
from pygrametl.declarativeetl.PygrametlGenerator import PygramGenerator
from pygrametl.declarativeetl.parsing import IntermediateSpecification


def create(spec_filepath):
    spec = IntermediateSpecification(spec_filepath)
    generate_pygram(spec)
    generate_ddl(spec)


def generate_pygram(spec):
    generator = PygramGenerator()
    generator.create_pygrametl_file(spec)


def generate_ddl(spec):
    ddl_generator = DDLGenerator(spec)
    ddl_generator.make_ddl_file()


if __name__ == "__main__":
    create(sys.argv[1])
