from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    api_keys = relationship("APIKey", back_populates="user")
    usage_records = relationship("UsageRecord", back_populates="user")
    subscriptions = relationship("Subscription", back_populates="user")


class APIKey(Base):
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    key_hash = Column(String, unique=True, index=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    last_used_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="api_keys")
    usage_records = relationship("UsageRecord", back_populates="api_key")


class UsageRecord(Base):
    __tablename__ = "usage_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    api_key_id = Column(Integer, ForeignKey("api_keys.id"))
    captcha_type = Column(String)  # text, math, image, etc.
    success = Column(Boolean)
    response_time_ms = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="usage_records")
    api_key = relationship("APIKey", back_populates="usage_records")


class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    plan_type = Column(String)  # free, basic, pro, enterprise
    status = Column(String)  # active, cancelled, expired
    current_period_start = Column(DateTime)
    current_period_end = Column(DateTime)
    solves_used = Column(Integer, default=0)
    solves_limit = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="subscriptions")


class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    razorpay_payment_id = Column(String, unique=True)
    amount = Column(Float)
    currency = Column(String, default="INR")
    status = Column(String)  # created, authorized, captured, failed
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User") 