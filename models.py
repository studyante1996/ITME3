from sqlalchemy import Column, Integer, String, DateTime, Boolean
from .database import Base

class Tool(Base):
    __tablename__ = "tools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    is_available = Column(Boolean, default=True)
    borrower_name = Column(String, nullable=True)
    borrow_time = Column(DateTime, nullable=True)
    return_time = Column(DateTime, nullable=True)
