from app import db
from datetime import datetime

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_type = db.Column(db.String(20), nullable=False)  # 'paypal' or 'mpesa'
    transaction_id = db.Column(db.String(100), unique=True)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)