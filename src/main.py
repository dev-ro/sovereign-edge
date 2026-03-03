import logging
import signal
import sys
import time
try:
    from src.mqtt_router import MQTTRouter
    from src.vector_store import VectorStore
    from src.inference_engine import InferenceEngine
except ImportError:
    from mqtt_router import MQTTRouter
    from vector_store import VectorStore
    from inference_engine import InferenceEngine

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("sovereign_edge")

class SovereignEdgeOrchestrator:
    def __init__(self, broker="localhost", db_path="data/telemetry_db"):
        self.router = MQTTRouter(broker=broker)
        self.store = VectorStore(db_path=db_path)
        self.engine = InferenceEngine()
        
        # wire callbacks
        self.router.on_telemetry_received = self._process_telemetry

    def _process_telemetry(self, topic, payload):
        logger.info(f"processing telemetry from {topic}")
        
        # 1. persist to vector db
        try:
            self.store.ingest(topic, payload)
        except Exception as e:
            logger.error(f"vector store ingestion failed: {e}")
            
        # 2. check for anomalies
        trigger_event = self.engine.check_anomaly(topic, payload)
        if trigger_event:
            logger.info(f"anomaly action: {trigger_event['reason']}")
            # discrete hook for local llm inference
            # in full autonomous state, this would trigger subprocess or async worker
            return trigger_event
        
        return None

    def start(self):
        logger.info("starting sovereign industrial edge pipeline")
        self.router.connect()

    def stop(self):
        logger.info("shutting down pipeline")
        self.router.disconnect()

if __name__ == "__main__":
    orchestrator = SovereignEdgeOrchestrator()
    orchestrator.start()
    
    def handle_sigterm(sig, frame):
        orchestrator.stop()
        sys.exit(0)
        
    signal.signal(signal.SIGINT, handle_sigterm)
    signal.signal(signal.SIGTERM, handle_sigterm)
    
    while True:
        time.sleep(1)
