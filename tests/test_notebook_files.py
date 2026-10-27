"""The student must be able to copy every block without editing imports."""
import ast
import json
import re
from pathlib import Path

def test_every_notebook_file_block_matches_implementation():
    root = Path(__file__).resolve().parents[1]
    notebook = json.loads((root / 'CodeDoctor.ipynb').read_text(encoding='utf-8'))
    count = 0
    for index, cell in enumerate(notebook['cells']):
        if cell['cell_type'] != 'code':
            continue
        heading = notebook['cells'][index - 1]['source']
        filename = re.search(r'Destination: `([^`]+)`', heading).group(1)
        source = cell['source']
        assert source == (root / filename).read_text(encoding='utf-8'), filename
        ast.parse(source)
        assert not cell['outputs'] and cell['execution_count'] is None
        count += 1
    assert count == 9
