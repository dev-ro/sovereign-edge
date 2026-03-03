import pytest
from src.inference_engine import InferenceEngine

def test_inference_engine_anomaly_detection():
    engine = InferenceEngine(thresholds={"temp": {"max": 30}})
    
    # normal value
    result = engine.check_anomaly("telemetry/temp", {"sensor": "temp", "value": 25})
    assert result is False
    
    # anomaly value
    result = engine.check_anomaly("telemetry/temp", {"sensor": "temp", "value": 35})
    assert result["status"] == "triggered"
    assert result["sensor"] == "temp"
    assert result["value"] == 35

def test_inference_engine_vibration_threshold():
    engine = InferenceEngine() # use default thresholds
    
    # abnormal vibration
    result = engine.check_anomaly("telemetry/motor", {"sensor": "vibration", "value": 12.0})
    assert result["status"] == "triggered"
    assert result["value"] == 12.0
