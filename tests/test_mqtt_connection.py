import pytest
from src.mqtt_router import MQTTRouter
import json
from unittest.mock import MagicMock

def test_mqtt_router_parsing():
    router = MQTTRouter()
    mock_callback = MagicMock()
    router.on_telemetry_received = mock_callback
    
    # simulate message
    class MockMsg:
        def __init__(self, topic, payload):
            self.topic = topic
            self.payload = payload
            
    test_payload = {"sensor": "temp", "value": 24.5}
    msg = MockMsg("telemetry/temp", json.dumps(test_payload).encode())
    
    router._on_message(None, None, msg)
    
    mock_callback.assert_called_once_with("telemetry/temp", test_payload)

def test_mqtt_router_connect_logic(mocker):
    mock_client = mocker.patch("paho.mqtt.client.Client")
    router = MQTTRouter(broker="test_broker", port=1234)
    router.connect()
    
    router.client.connect.assert_called_once_with("test_broker", 1234, 60)
    router.client.loop_start.assert_called_once()
