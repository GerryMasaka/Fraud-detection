from typing import List, Union

from pydantic import BaseModel


class FraudBase(BaseModel):
    id: int

class FraudCreate(FraudBase):
    id: int
    customer_id: float
    terminal_id: float
    amount:float
    tx_time_seconds:float
    tx_time_days:float
    tx_weekend:float
    tx_night:float
    customer_id_tx_1day:float
    customer_id_avg_1day:float
    customer_id_tx_7day:float
    customer_id_avg_7day:float
    customer_id_tx_30day:float
    customer_id_avg_30day:float
    terminal_id_tx_1day:float
    terminal_id_risk_1day:float
    terminal_id_tx_7day:float
    terminal_id_risk_7day:float
    terminal_id_tx_30day:float
    terminal_id_risk_30day:float

class Fraud(FraudBase):
    id:int
    customer_id: float
    terminal_id: float
    amount:float
    tx_time_seconds:float
    tx_time_days:float
    tx_weekend:float
    tx_night:float
    customer_id_tx_1day:float
    customer_id_avg_1day:float
    customer_id_tx_7day:float
    customer_id_avg_7day:float
    customer_id_tx_30day:float
    customer_id_avg_30day:float
    terminal_id_tx_1day:float
    terminal_id_risk_1day:float
    terminal_id_tx_7day:float
    terminal_id_risk_7day:float
    terminal_id_tx_30day:float
    terminal_id_risk_30day:float

    class Config:
        orm_mode = True




