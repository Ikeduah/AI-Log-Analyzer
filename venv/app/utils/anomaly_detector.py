from sklearn.ensemble import IsolationForest

def detect_anomalies(df):
    df["minute"] = df["timestamp"].dt.floor("T")
    counts = df.groupby("minute").size().reset_index(name="count")

    model = IsolationForest(contamination=0.05, random_state=42)
    counts["anomaly"] = model.fit_predict(counts[["count"]])

    anomalies = counts[counts["anomaly"] == -1]
    return anomalies