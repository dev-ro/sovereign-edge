import logging

logger = logging.getLogger(__name__)

class InferenceEngine:
    def __init__(self, thresholds=None):
        # default thresholds for critical sensors
        self.thresholds = thresholds or {
            "temp": {"min": 0, "max": 40},
            "humidity": {"min": 20, "max": 80},
            "vibration": {"max": 5.0}
        }
        self.trigger_count = 0

    def check_anomaly(self, topic, payload):
        sensor = payload.get("sensor")
        value = payload.get("value")
        
        if sensor in self.thresholds:
            limits = self.thresholds[sensor]
            is_anomaly = False
            
            if "min" in limits and value < limits["min"]:
                is_anomaly = True
            if "max" in limits and value > limits["max"]:
                is_anomaly = True
                
            if is_anomaly:
                logger.warning(f"anomaly detected for {sensor}: {value} is out of bounds {limits}")
                return self._trigger_llm(sensor, value, limits)
        
        return False

    def _trigger_llm(self, sensor, value, limits):
        self.trigger_count += 1
        logger.info(f"triggering local llm inference for {sensor} anomaly")
        # mock local llm trigger logic
        # in production, this would hand off to a quantized instance (llama-cpp-python, etc)
        # for now, we return a structured trigger event
        return {
            "status": "triggered",
            "sensor": sensor,
            "value": value,
            "limits": limits,
            "reason": f"{sensor} value {value} violated limits {limits}"
        }
