from sqlalchemy import create_engine, Column, Integer, Float, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///fraud_logs.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class FraudLog(Base):
    __tablename__ = "fraud_logs"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    prediction = Column(String)
    probability = Column(Float)
    is_night = Column(Boolean)
    new_device = Column(Boolean)
    location_changed = Column(Boolean)
    transactions_today = Column(Integer)

Base.metadata.create_all(bind=engine)
