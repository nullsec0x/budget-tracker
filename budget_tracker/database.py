from sqlalchemy import create_engine, Column, Integer, String, Float, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import os

Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String)
    date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Transaction({self.type}, {self.amount}, {self.category})>"

class Settings(Base):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True)
    currency_symbol = Column(String, default='$')
    monthly_budget = Column(Float, default=0.0)
    savings_goal_amount = Column(Float, default=0.0)
    savings_goal_name = Column(String, default='Savings Goal')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

def init_db():
    engine = create_engine('sqlite:///budget.db', echo=False)
    Base.metadata.create_all(engine)
    return engine

def get_session():
    engine = init_db()
    Session = sessionmaker(bind=engine)
    return Session()
