from sqlalchemy import Column, Integer, Float

from app.Database.database import Base

class Fraud(Base):
    __tablename__ = "frauds"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Float)
    terminal_id = Column(Float)
    amount=Column(Float)
    tx_time_seconds=Column(Float)
    tx_time_days=Column(Float)
    tx_weekend=Column(Float)
    tx_night=Column(Float)
    customer_id_tx_1day=Column(Float)
    customer_id_avg_1day=Column(Float)
    customer_id_tx_7day=Column(Float)
    customer_id_avg_7day=Column(Float)
    customer_id_tx_30day=Column(Float)
    customer_id_avg_30day=Column(Float)
    terminal_id_tx_1day=Column(Float)
    terminal_id_risk_1day=Column(Float)
    terminal_id_tx_7day=Column(Float)
    terminal_id_risk_7day=Column(Float)
    terminal_id_tx_30day=Column(Float)
    terminal_id_risk_30day=Column(Float)







