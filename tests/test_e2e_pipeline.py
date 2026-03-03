import pytest
from src.main import SovereignEdgeOrchestrator
from unittest.mock import MagicMock

@pytest.fixture
def orchestrator(tmp_path):
    db_path = tmp_path / "e2e_db"
    return SovereignEdgeOrchestrator(broker="mock_broker", db_path=str(db_path))

def test_e2e_pipeline_routing(orchestrator, mocker):
    # mock mqtt message ingestion
    test_payload = {"sensor": "temp", "value": 45.0} # should trigger anomaly (max 40)
    topic = "telemetry/server_room"
    
    # process the mock telemetry
    trigger_event = orchestrator._process_telemetry(topic, test_payload)
    
    # verify vector storage (check if table exists and has data)
    table_names = orchestrator.store.db.table_names()
    assert "telemetry" in table_names
    
    # verify anomaly trigger
    assert trigger_event is not None
    assert trigger_event["status"] == "triggered"
    assert trigger_event["sensor"] == "temp"
    assert "violated limits" in trigger_event["reason"]

def test_e2e_normal_operation(orchestrator):
    test_payload = {"sensor": "temp", "value": 25.0} # normal
    topic = "telemetry/office"
    
    trigger_event = orchestrator._process_telemetry(topic, test_payload)
    
    # should NOT trigger
    assert trigger_event is None
    
    # verify persistence
    results = orchestrator.store.search("office temperature")
    assert len(results) > 0
    assert results[0]["value"] == 25.0
