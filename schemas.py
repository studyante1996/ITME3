from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ToolBase(BaseModel):
    name: str
    description: str

class ToolCreate(ToolBase):
    pass

class Tool(ToolBase):
    id: int
    is_available: bool
    borrower_name: Optional[str] = None
    borrow_time: Optional[datetime] = None
    return_time: Optional[datetime] = None

    class Config:
        orm_mode = True
