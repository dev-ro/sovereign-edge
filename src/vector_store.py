import lancedb
import pandas as pd
import os
from sentence_transformers import SentenceTransformer
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, db_path="data/telemetry_db", model_name="all-MiniLM-L6-v2"):
        self.db_path = db_path
        self.db = lancedb.connect(db_path)
        self.model = SentenceTransformer(model_name)
        self.table_name = "telemetry"

    def _ensure_table(self, data_sample):
        if self.table_name not in self.db.table_names():
            self.db.create_table(self.table_name, data=data_sample)

    def ingest(self, topic, payload):
        text = f"topic: {topic} sensor: {payload.get('sensor')} value: {payload.get('value')}"
        embedding = self.model.encode(text).tolist()
        
        data = {
            "timestamp": [datetime.now().isoformat()],
            "topic": [topic],
            "sensor": [payload.get("sensor")],
            "value": [payload.get("value")],
            "vector": [embedding]
        }
        df = pd.DataFrame(data)
        
        if self.table_name not in self.db.table_names():
            self.db.create_table(self.table_name, data=df)
        else:
            table = self.db.open_table(self.table_name)
            table.add(df)
        
        logger.info(f"ingested {topic} into lancedb")

    def search(self, query, limit=5):
        embedding = self.model.encode(query).tolist()
        table = self.db.open_table(self.table_name)
        return table.search(embedding).limit(limit).to_list()
