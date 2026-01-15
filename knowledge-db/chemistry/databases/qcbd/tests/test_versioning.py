from pathlib import Path
from expert.versioning import create_snapshot, SNAPSHOT_DIR

def test_snapshot_creation():
    path = create_snapshot('test')
    assert path.exists()
    assert path.parent == SNAPSHOT_DIR
