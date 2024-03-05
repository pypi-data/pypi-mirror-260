from pathlib import Path
from gfatpy.utils.io import read_yaml

SCC_INFO = read_yaml(Path(__file__).parent.absolute() / "info.yml")
MAX_EXEC_TIME = int(1200)  # 3600

__all__ = ["SCC_INFO", "MAX_EXEC_TIME"]
