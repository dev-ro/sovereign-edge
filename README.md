# sovereign-edge

local-first telemetry and inference pipeline. zero cloud dependency.

## architecture

- **python core logic router**: orchestrates telemetry streams.
- **mqtt**: high-throughput, low-latency message brokering (paho-mqtt).
- **lancedb**: local vector embedding storage for telemetry persistence.
- **inference**: quantized llm triggers on anomaly detection.

## core logic

- **deterministic routing**: mqtt streams telemetry $\rightarrow$ python ingests $\rightarrow$ lancedb embeds $\rightarrow$ llm triggers on anomaly.
- **zero cloud**: all inference and storage execute locally.
- **modular design**: hot-swap quantized models without breaking the mqtt pipeline.

## quickstart

### dependencies
```bash
python -m venv venv
source venv/bin/activate  # venv\Scripts\activate on windows
pip install -r requirements.txt
```

### verification
```bash
python -m pytest tests/
```

### execution
```bash
python src/main.py
```

## license
mit
