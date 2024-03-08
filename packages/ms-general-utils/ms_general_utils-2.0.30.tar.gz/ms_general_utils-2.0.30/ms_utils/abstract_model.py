"""
Abstract Base Model
"""

from sqlalchemy import Column, DateTime, Integer, func


class BaseModel:
    """
    Datetime created_at and updated_at
    """
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=func.CURRENT_TIMESTAMP())
    updated_at = Column(DateTime, default=func.CURRENT_TIMESTAMP(), onupdate=func.CURRENT_TIMESTAMP())
