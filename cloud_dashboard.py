
import streamlit as st
import pandas as pd
import joblib
import time
from datetime import datetime

st.set_page_config(
    page_title="5G MEC AI Security",
    page_icon="🛡️",
    layout="wide"
)

FEATURES = [
    "packet_rate",
    "latency_ms",
    "throughput_mbps",
    "packet_loss_pct",
    "session_count"
]

@st.cache_resource
def load_model():
    saved = joblib.load("ue_anomaly_model.pkl")
    return saved["model"]

@st.cache_data
def load_dataset():
    return pd.read_csv("ue_behavior_dataset.csv")

model = load_model()
df = load_dataset()

st.title("🛡️ 5G MEC AI Security Dashboard")
st.caption(
    "AI-Based UE Anomaly Detection | "
    "5G MEC Security Research Prototype"
)

st.info(
    "Public demonstration using synthetic UE observations. "
    "The AI is not deployed on an operational 5G network."
)

st.subheader("Dataset Overview")

c1, c2, c3 = st.columns(3)

c1.metric("Total Observations", len(df))
c2.metric("Normal Labels", (df["label"] == 0).sum())
c3.metric("Suspicious Labels", (df["label"] == 1).sum())

st.divider()

st.subheader("Live Simulated UE Monitoring")

count = st.slider(
    "Number of observations",
    min_value=5,
    max_value=100,
    value=20,
    step=5
)

delay = st.slider(
    "Interval between observations (seconds)",
    min_value=0.2,
    max_value=2.0,
    value=0.5,
    step=0.1
)

metrics_area = st.empty()
results_area = st.empty()
alerts_area = st.empty()
progress_area = st.empty()

if st.button("Start AI Monitoring", type="primary"):

    normal_count = round(count * 0.8)
    suspicious_count = count - normal_count

    normal = df[df["label"] == 0].sample(
        n=normal_count,
        random_state=42
    )

    suspicious = df[df["label"] == 1].sample(
        n=suspicious_count,
        random_state=42
    )

    samples = pd.concat(
        [normal, suspicious],
        ignore_index=True
    ).sample(
        frac=1,
        random_state=42
    )

    results = []

    for index, (_, row) in enumerate(samples.iterrows()):

        input_data = pd.DataFrame(
            [[row[f] for f in FEATURES]],
            columns=FEATURES
        )

        start = time.perf_counter()

        prediction = int(model.predict(input_data)[0])
        decision_score = float(
            model.decision_function(input_data)[0]
        )

        inference_ms = (
            time.perf_counter() - start
        ) * 1000

        risk_score = round(
            min(100, max(0, -decision_score * 400)),
            2
        )

        if risk_score >= 70:
            risk_level = "HIGH"
            action = "Security review recommended"

        elif risk_score >= 30:
            risk_level = "MEDIUM"
            action = "Investigate and increase monitoring"

        elif prediction == -1:
            risk_level = "LOW"
            action = "Anomaly detected - monitor and review"

        else:
            risk_level = "LOW"
            action = "Continue normal monitoring"

        ai_prediction = (
            "ANOMALY" if prediction == -1 else "NORMAL"
        )

        results.append({
            "Timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "UE ID": row["ue_id"],
            "AI Prediction": ai_prediction,
            "Risk Score": risk_score,
            "Risk Level": risk_level,
            "Recommended Action": action,
            "Inference Time (ms)": round(inference_ms, 3)
        })

        result_df = pd.DataFrame(results)

        normal_total = (
            result_df["AI Prediction"] == "NORMAL"
        ).sum()

        anomaly_total = (
            result_df["AI Prediction"] == "ANOMALY"
        ).sum()

        high_total = (
            result_df["Risk Level"] == "HIGH"
        ).sum()

        with metrics_area.container():

            a, b, c, d = st.columns(4)

            a.metric("Processed", len(results))
            b.metric("Normal", normal_total)
            c.metric("Anomalies", anomaly_total)
            d.metric("High Risk", high_total)

        with results_area.container():

            st.subheader("AI Prediction Results")

            st.dataframe(
                result_df.iloc[::-1],
                use_container_width=True,
                hide_index=True
            )

        with alerts_area.container():

            st.subheader("Security Alerts")

            alerts = result_df[
                result_df["AI Prediction"] == "ANOMALY"
            ]

            if not alerts.empty:

                st.warning(
                    f"{len(alerts)} anomalous "
                    "observations detected"
                )

                st.dataframe(
                    alerts.iloc[::-1],
                    use_container_width=True,
                    hide_index=True
                )

            else:
                st.success("No anomalies detected so far")

        progress_area.progress(
            (index + 1) / len(samples)
        )

        time.sleep(delay)

    st.success("AI monitoring completed!")

    st.download_button(
        "Download Monitoring Results",
        data=pd.DataFrame(results).to_csv(index=False),
        file_name="ue_monitoring_results.csv",
        mime="text/csv"
    )

st.divider()

st.caption(
    "Isolation Forest anomaly detection | "
    "Synthetic data | Experimental risk scoring | "
    "No automatic UE blocking"
)
