import sys

from pygrametl.declarativeetl.DDLGenerator import DDLGenerator
from pygrametl.declarativeetl.PygrametlGenerator import PygramGenerator
from pygrametl.declarativeetl.parsing import IntermediateSpecification
from pygrametl.declarativeetl import create_source_files


if __name__ == "__main__":
    # create(sys.argv[1])
    create_source_files(sys.argv[1])
