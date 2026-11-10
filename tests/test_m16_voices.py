"""Hangprofilok: a törölt alaphang nem jön vissza újraindításkor, a törlés a referenciafájlt is viszi."""

from fastapi.testclient import TestClient

from app.main import create_app
from app.state import AppState
from tests.test_m3_jobs_export import make_state


def test_deleted_default_voice_stays_deleted(config):
    st = make_state(config)
    with TestClient(create_app(st)) as client:
        assert client.delete("/api/voices/piper-berta").status_code == 200
    again = AppState(config)
    assert again.repo.get_voice("piper-berta") is None


def test_delete_removes_reference_file(config):
    st = make_state(config)
    ref = config.paths.voices_dir / "sajat.wav"
    ref.write_bytes(b"RIFF")
    st.repo.upsert_voice("sajat", "Saját", "f5_hu", str(ref), "szöveg", {})
    with TestClient(create_app(st)) as client:
        assert client.delete("/api/voices/sajat").status_code == 200
    assert not ref.exists()
