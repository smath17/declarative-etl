import sys

from pygrametl.declarativespecification.DDLGenerator import DDLGenerator
from pygrametl.declarativespecification.PygramGenerator import PygramGenerator
from pygrametl.declarativespecification.parsing import IntermediateSpecification


def create(spec_filepath):
    spec = IntermediateSpecification(spec_filepath)
    generate_pygram(spec)
    generate_ddl(spec)


def generate_pygram(spec):
    generator = PygramGenerator(spec)
    generator.create_pygram_file(spec)


def generate_ddl(spec):
    ddl_generator = DDLGenerator(spec)
    ddl_generator.make_ddl_file()


if __name__ == "__main__":
    create(sys.argv[1])
