import json
from pathlib import Path

MANIFEST = Path(__file__).parent.parent / "extension" / "manifest.json"

def test_manifest_exists():
    assert MANIFEST.exists()

def test_manifest_is_v3():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data["manifest_version"] == 3

def test_manifest_declares_sandbox():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert "sandbox" in data and "sandbox.html" in data["sandbox"]["pages"]

def test_manifest_host_permissions_local_only():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for hp in data.get("host_permissions", []):
        assert "127.0.0.1" in hp or "localhost" in hp