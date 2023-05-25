from pygrametl.declarativespecification.DDLGenerator import DDLGenerator
from pygrametl.declarativespecification.PygramGenerator import PygramGenerator
from pygrametl.declarativespecification.parsing import IntermediateSpecification


def main():
    spec = IntermediateSpecification('test-toml.txt')
    generator = PygramGenerator(spec)
    generator.create_pygram_file(spec)
    ddl_generator = DDLGenerator(spec)
    ddl_generator.make_ddl_file()


if __name__ == "__main__":
    main()
