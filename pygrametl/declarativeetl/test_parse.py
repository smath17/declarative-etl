import sys
from pygrametl.declarativeetl import create_source_files


if __name__ == "__main__":
    create_source_files(sys.argv[1])
