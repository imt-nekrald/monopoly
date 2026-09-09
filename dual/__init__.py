import sys
import pathlib 

_file_path: pathlib.Path = pathlib.Path(__file__)
sys.path.append(str(_file_path.absolute().parent))
sys.path.append(str(_file_path.absolute().parent.parent))