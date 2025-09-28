from flask import Blueprint, request, jsonify
from .utils.log_parser import parse_log
from .utils.anomaly_detector import detect_anomalies
from .models import db, LogEntry, Anomaly

main_bp = Blueprint("main", __name__)

@main_bp.route("/upload-log", methods=["POST"])
def upload_log():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    df_logs = parse_log(file)

    # Save log entries
    log_entries = []
    for _, row in df_logs.iterrows():
        log = LogEntry(timestamp=row["timestamp"], level=row["level"], message=row["message"])
        log_entries.append(log)
    db.session.add_all(log_entries)
    db.session.commit()

    # Detect anomalies
    anomalies_df = detect_anomalies(df_logs)
    anomalies = []
    for _, row in anomalies_df.iterrows():
        log = log_entries[row.name]  # match by index
        anomaly = Anomaly(log_entry_id=log.id, anomaly_type="Frequency Spike")
        anomalies.append(anomaly)
    db.session.add_all(anomalies)
    db.session.commit()

    return jsonify({
        "message": "File processed",
        "anomalies": [{"id": a.id, "log_entry_id": a.log_entry_id} for a in anomalies]
    })