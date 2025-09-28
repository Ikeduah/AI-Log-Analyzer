from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class LogEntry(db.Model):
    __tablename__ = "log_entries"
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    level = db.Column(db.String(10), nullable=False)
    message = db.Column(db.Text, nullable=False)
    uploaded_at = db.Column(db.DateTime, server_default=db.func.now())

class Anomaly(db.Model):
    __tablename__ = "anomalies"
    id = db.Column(db.Integer, primary_key=True)
    log_entry_id = db.Column(db.Integer, db.ForeignKey("log_entries.id"))
    anomaly_type = db.Column(db.String(50))
    detected_at = db.Column(db.DateTime, server_default=db.func.now())

    log_entry = db.relationship("LogEntry", backref="anomalies")