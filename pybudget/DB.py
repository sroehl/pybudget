from sqlalchemy import create_engine, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
Session = None

# Flow Globals
EXPENSE = 0
INCOME = 1


class Budget(Base):
    __tablename__ = 'budget'

    id = Column(Integer, primary_key=True)
    month = Column(String)
    name = Column(String)
    amount = Column(Float)
    flow = Column(Integer, default=EXPENSE)


class Transactions(Base):
    __tablename__ = 'transactions'
    __table_args__ = (
        UniqueConstraint('date', 'month', 'vendor', 'amount', name='unique_transaction'),
    )
    id = Column(Integer, primary_key=True)
    date = Column(String)
    month = Column(String)
    vendor = Column(String)
    amount = Column(Float)
    notes = Column(String)
    flow = Column(Integer, default=EXPENSE)
    category = Column(String)
    imported_vendor = Column(String)


class CategoryRules(Base):
    __tablename__ = 'categoryrules'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)


def get_session():
    global Session
    if Session is None:
        Session = sessionmaker(bind=engine)
    return Session()


engine = create_engine('sqlite:///budget.db', echo=False)
Base.metadata.create_all(engine)
