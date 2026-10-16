
# AI-Driven 5G MEC Framework for Intelligent Security and QoS Management

## Project Overview

This project proposes an AI-based security monitoring layer for 5G Multi-access Edge Computing (MEC) environments.

The current prototype uses an Isolation Forest machine learning model to detect anomalous User Equipment (UE) behavior based on network performance and session-related features.

## Features

- AI-based UE anomaly detection
- Experimental risk scoring (0–100)
- LOW, MEDIUM and HIGH risk classification
- Live simulated UE monitoring
- Security alerts and recommended actions
- Downloadable monitoring results
- Interactive Streamlit dashboard

## Technologies

- Python
- Scikit-learn (Isolation Forest)
- Pandas and NumPy
- Streamlit
- FastAPI (local API prototype)

## Input Features

1. Packet rate
2. Latency (ms)
3. Throughput (Mbps)
4. Packet loss (%)
5. Session count

## How It Works

Synthetic UE observations
→ Isolation Forest anomaly detection
→ Experimental risk assessment
→ Security alerts
→ Dashboard visualization

## Current Implementation

The prototype has been implemented and tested locally using synthetic data.

The public dashboard runs the trained model directly within Streamlit.

The existing FastAPI service is available as a separate local prototype.

## Limitations

- Uses synthetic data rather than operational 5G traffic.
- Not deployed on a real MEC server.
- Risk scores are heuristic indicators, not fraud probabilities.
- No automatic UE blocking or real network policy enforcement.
- QoS-aware security monitoring is demonstrated, but integration with 5G core policy functions remains future work.

## Future Work

- Deployment on a MEC-compatible edge environment
- Integration with 5G network telemetry
- Validation using representative real-world datasets
- Integration with network policy and security workflows
- Evaluation of latency, detection accuracy and scalability

## Disclaimer

This is a research demonstration. It does not represent an operational telecom security system.
