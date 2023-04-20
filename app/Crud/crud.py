from sqlalchemy.orm import Session
import logging
from app.Schema import schemas
from app.Models import models


def get_fraud(db: Session, Fraud_id: int):
    return db.query(models.Fraud).filter(models.Fraud.id == Fraud_id).first()


def get_fraud(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Fraud).offset(skip).limit(limit).all()


def create_fraud(db: Session, fraud: schemas.FraudCreate):
    data_model = models.Fraud()
    data_model.CUSTOMER_ID = fraud.customer_id
    data_model.TERMINAL_ID = fraud.terminal_id
    data_model.TX_AMOUNT = fraud.amount
    data_model.TX_TIME_SECONDS = fraud.tx_time_seconds
    data_model.TX_TIME_DAYS = fraud.tx_time_days
    data_model.TX_DURING_WEEKEND = fraud.tx_weekend
    data_model.TX_DURING_NIGHT = fraud.tx_night
    data_model.CUSTOMER_ID_NB_TX_1DAY_WINDOW = fraud.customer_id_tx_1day
    data_model.CUSTOMER_ID_AVG_AMOUNT_1DAY_WINDOW= fraud.customer_id_avg_1day
    data_model.CUSTOMER_ID_NB_TX_7DAY_WINDOW = fraud.customer_id_tx_7day
    data_model.CUSTOMER_ID_AVG_AMOUNT_7DAY_WINDOW= fraud.customer_id_avg_7day
    data_model.CUSTOMER_ID_NB_TX_30DAY_WINDOW = fraud.customer_id_tx_30day
    data_model.CUSTOMER_ID_AVG_AMOUNT_30DAY_WINDOW = fraud.customer_id_avg_30day
    data_model.TERMINAL_ID_NB_TX_1DAY_WINDOW = fraud.terminal_id_tx_1day
    data_model.TERMINAL_ID_RISK_1DAY_WINDOW = fraud.terminal_id_risk_1day
    data_model.TERMINAL_ID_NB_TX_7DAY_WINDOW = fraud.terminal_id_tx_7day
    data_model.TERMINAL_ID_RISK_7DAY_WINDOW = fraud.terminal_id_risk_7day
    data_model.TERMINAL_ID_NB_TX_30DAY_WINDOW = fraud.terminal_id_tx_30day
    data_model.TERMINAL_ID_RISK_30DAY_WINDOW = fraud.terminal_id_risk_30day
    db.add(data_model)
    db.commit()
    db.refresh(data_model)
    logging.info(msg=f"DATA MODEL{data_model}")   
    return data_model


