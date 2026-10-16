import io, json
from pathlib import Path
import pytest

pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

from backend.app import create_app


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("SF_UPLOADS", str(tmp_path / "jobs"))
    app = create_app()
    with TestClient(app) as c:
        yield c


def _png_bytes():
    import numpy as np, cv2
    img = np.zeros((64, 64, 3), dtype=np.uint8)
    img[10:50, 10:50] = 255
    ok, buf = cv2.imencode(".png", img)
    assert ok
    return buf.tobytes()


def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_generate_requires_image(client):
    r = client.post("/api/generate", data={"style": "outline"})
    assert r.status_code == 422


def test_generate_rejects_unknown_style(client):
    files = {"image": ("t.png", _png_bytes(), "image/png")}
    r = client.post("/api/generate", files=files, data={"style": "nope"})
    assert r.status_code in (400, 500)


def test_generate_end_to_end(client):
    files = {"image": ("t.png", _png_bytes(), "image/png")}
    r = client.post("/api/generate", files=files, data={"style": "outline"})
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["status"] == "done"
    job_id = data["job_id"]

    # Job status
    r2 = client.get(f"/api/jobs/{job_id}")
    assert r2.status_code == 200

    # Preview file
    r3 = client.get(f"/api/jobs/{job_id}/files/index.html")
    assert r3.status_code == 200
    assert "<!doctype html>" in r3.text.lower()

    # Bundle zip
    r4 = client.get(f"/api/jobs/{job_id}/bundle")
    assert r4.status_code == 200
    assert r4.headers["content-type"] == "application/zip"


def test_job_not_found(client):
    r = client.get("/api/jobs/doesnotexist")
    assert r.status_code == 404