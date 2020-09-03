import json
from pathlib import Path

fpath = Path(__file__).parent.resolve() / "QCSchema.schema"
qcschema = json.loads(fpath.read_text())
