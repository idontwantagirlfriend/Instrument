from pathlib import Path

from main import parseFile
path = "test/text_fr.txt"

pathified = Path(path)

parseFile(path, str(pathified.parent/Path(str(pathified.stem)+"_result.txt")))
