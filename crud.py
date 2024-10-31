from sqlalchemy.orm import Session
from datetime import datetime
from . import models, schemas

def create_tool(db: Session, tool: schemas.ToolCreate):
    db_tool = models.Tool(**tool.dict())
    db.add(db_tool)
    db.commit()
    db.refresh(db_tool)
    return db_tool

def get_tools(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Tool).offset(skip).limit(limit).all()

def get_tool(db: Session, tool_id: int):
    return db.query(models.Tool).filter(models.Tool.id == tool_id).first()

def update_tool(db: Session, tool_id: int, tool: schemas.ToolCreate):
    db_tool = get_tool(db, tool_id)
    if db_tool:
        for key, value in tool.dict().items():
            setattr(db_tool, key, value)
        db.commit()
        db.refresh(db_tool)
    return db_tool

def delete_tool(db: Session, tool_id: int):
    db_tool = get_tool(db, tool_id)
    if db_tool:
        db.delete(db_tool)
        db.commit()
        return True
    return False

def borrow_tool(db: Session, tool_id: int, borrower_name: str):
    db_tool = get_tool(db, tool_id)
    if db_tool and db_tool.is_available:
        db_tool.is_available = False
        db_tool.borrower_name = borrower_name
        db_tool.borrow_time = datetime.now()
        db_tool.return_time = None
        db.commit()
        db.refresh(db_tool)
        return db_tool
    return None

def return_tool(db: Session, tool_id: int):
    db_tool = get_tool(db, tool_id)
    if db_tool and not db_tool.is_available:
        db_tool.is_available = True
        db_tool.return_time = datetime.now()
        db.commit()
        db.refresh(db_tool)
        return db_tool
    return None

def get_available_tools(db: Session):
    return db.query(models.Tool).filter(models.Tool.is_available == True).all()

def get_borrowed_tools(db: Session):
    return db.query(models.Tool).filter(models.Tool.is_available == False).all()

def get_tool_by_name(db: Session, name: str):
    return db.query(models.Tool).filter(models.Tool.name == name).first()
