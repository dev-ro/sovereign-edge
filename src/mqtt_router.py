import paho.mqtt.client as mqtt
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MQTTRouter:
    def __init__(self, broker="localhost", port=1883, client_id="sovereign_router"):
        self.broker = broker
        self.port = port
        self.client_id = client_id
        self.client = mqtt.Client(client_id=client_id, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
        
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.on_telemetry_received = None

    def _on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            logger.info(f"connected to broker {self.broker}:{self.port}")
            client.subscribe("telemetry/#")
        else:
            logger.error(f"connection failed with code {rc}")

    def _on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            logger.info(f"received message on {msg.topic}: {payload}")
            if self.on_telemetry_received:
                self.on_telemetry_received(msg.topic, payload)
        except Exception as e:
            logger.error(f"failed to parse message: {e}")

    def connect(self):
        import time
        retry_delay = 1
        max_delay = 60
        while True:
            try:
                self.client.connect(self.broker, self.port, 60)
                self.client.loop_start()
                logger.info("mqtt loop started")
                break
            except Exception as e:
                logger.error(f"connection failed: {e}. retrying in {retry_delay}s...")
                time.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, max_delay)

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

if __name__ == "__main__":
    router = MQTTRouter()
    router.connect()
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        router.disconnect()
