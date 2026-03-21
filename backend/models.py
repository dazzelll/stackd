from sqlalchemy import Column, String, Integer, Numeric, Boolean, Date, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String)
    real_age = Column(Integer)
    mode = Column(String, default='growth')  # 'growth' | 'frugal'
    caught_alerts = Column(JSON, nullable=True) # For the Caught in 4K alerts
    created_at = Column(DateTime, default=func.now())
    total_debt = Column(Numeric(precision=12, scale=2), default=0.0) 

class PlaidItem(Base):
    __tablename__ = "plaid_items"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"))
    access_token = Column(String, nullable=False)
    item_id = Column(String)
    institution_name = Column(String)
    created_at = Column(DateTime, default=func.now())

class PortfolioSnapshot(Base):
    __tablename__ = "portfolio_snapshots"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"))
    snapshot_date = Column(Date, default=func.current_date())
    total_wealth = Column(Numeric(15, 2))
    stocks = Column(Numeric(15, 2), default=0)
    real_estate = Column(Numeric(15, 2), default=0)
    savings = Column(Numeric(15, 2), default=0)
    crypto = Column(Numeric(15, 2), default=0)
    bonds = Column(Numeric(15, 2), default=0)
    health_score = Column(Integer)
    created_at = Column(DateTime, default=func.now())

class Goal(Base):
    __tablename__ = "goals"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    title = Column(String, nullable=False)
    target_amount = Column(Numeric(15, 2))
    current_amount = Column(Numeric(15, 2), default=0.0)
    emoji = Column(String, default="🎯")
    deadline = Column(String, nullable=True) # Changed from Date to String so "Dec 2027" works!
    category = Column(String) 
    created_at = Column(DateTime, default=func.now())

class VillainArcEvent(Base):
    __tablename__ = "villain_arc_events"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"))
    transaction_id = Column(String)
    description = Column(String)
    amount = Column(Numeric(15, 2))
    emotion = Column(String)
    notes = Column(String)
    event_date = Column(Date)
    created_at = Column(DateTime, default=func.now())

class Streak(Base):
    __tablename__ = "streaks"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"))
    streak_type = Column(String)
    current_count = Column(Integer, default=0)
    best_count = Column(Integer, default=0)
    last_updated = Column(Date, default=func.current_date())
    created_at = Column(DateTime, default=func.now())

class Challenge(Base):
    __tablename__ = "challenges"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"))
    title = Column(String)
    description = Column(String)
    reward_points = Column(Integer)
    progress = Column(Integer, default=0)
    total = Column(Integer)
    emoji = Column(String)
    completed = Column(Boolean, default=False)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=func.now())

class ManualAssetLog(Base):
    __tablename__ = "manual_asset_logs"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    category = Column(String)
    label = Column(String)
    amount = Column(Numeric(15, 2))
    created_at = Column(DateTime, default=func.now())

class FinverseItem(Base):
    __tablename__ = "finverse_items"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    access_token = Column(String, nullable=False)
    item_id = Column(String)
    institution_name = Column(String)
    institution_id = Column(String)
    status = Column(String, default="active")  # active, error, expired
    last_sync = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    expires_at = Column(DateTime)

class BankAccount(Base):
    __tablename__ = "bank_accounts"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    finverse_item_id = Column(String, ForeignKey("finverse_items.id"))
    account_id = Column(String, nullable=False)
    account_name = Column(String)
    account_type = Column(String)  # checking, savings, credit, etc.
    account_subtype = Column(String)
    mask = Column(String)  # Last 4 digits
    status = Column(String, default="active")
    currency = Column(String, default="SGD")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())

class BankBalance(Base):
    __tablename__ = "bank_balances"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    account_id = Column(String, ForeignKey("bank_accounts.id"))
    balance_type = Column(String)  # current, available, ledger
    amount = Column(Numeric(15, 2))
    currency = Column(String, default="SGD")
    as_of_date = Column(DateTime)
    created_at = Column(DateTime, default=func.now())

class BankTransaction(Base):
    __tablename__ = "bank_transactions"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    account_id = Column(String, ForeignKey("bank_accounts.id"))
    transaction_id = Column(String, nullable=False)
    amount = Column(Numeric(15, 2))
    currency = Column(String, default="SGD")
    date = Column(Date)
    name = Column(String)
    description = Column(String)
    category = Column(String)
    pending = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
