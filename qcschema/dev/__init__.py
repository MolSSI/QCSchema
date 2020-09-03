import json

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

fpath = Path(__file__).parent.resolve() / "QCSchema.schema"
qcschema = json.loads(fpath.read_text())
