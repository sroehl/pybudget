from sqlalchemy import create_engine, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

Base = declarative_base()
Session = None

# Flow Globals
EXPENSE = 0
INCOME = 1


class Budget(Base):
    __tablename__ = 'budget'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
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
    user_id = Column(Integer, ForeignKey('user.id'))
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
    user_id = Column(Integer, ForeignKey('user.id'))
    name = Column(String)
    category = Column(String)


class User(UserMixin, Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


def get_session():
    global Session
    if Session is None:
        Session = sessionmaker(bind=engine)
    return Session()


engine = create_engine('sqlite:///budget.db', echo=False)
Base.metadata.create_all(engine)
