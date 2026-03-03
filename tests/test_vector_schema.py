import pytest
from src.vector_store import VectorStore
import os
import shutil

@pytest.fixture
def store(tmp_path):
    db_path = tmp_path / "test_db"
    return VectorStore(db_path=str(db_path))

def test_vector_store_ingestion(store):
    test_payload = {"sensor": "temp", "value": 24.5}
    store.ingest("telemetry/temp", test_payload)
    
    results = store.search("temperature")
    assert len(results) > 0
    assert results[0]["sensor"] == "temp"
    assert results[0]["value"] == 24.5

def test_vector_store_persistence(tmp_path):
    db_path = str(tmp_path / "persistent_db")
    store1 = VectorStore(db_path=db_path)
    store1.ingest("telemetry/hvac", {"sensor": "humidity", "value": 45})
    
    store2 = VectorStore(db_path=db_path)
    results = store2.search("humidity")
    assert len(results) > 0
    assert results[0]["sensor"] == "humidity"
