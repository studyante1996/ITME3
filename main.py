from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/tools/", response_model=schemas.Tool)
def create_tool(tool: schemas.ToolCreate, db: Session = Depends(get_db)):
    return crud.create_tool(db=db, tool=tool)

@app.get("/tools/", response_model=List[schemas.Tool])
def read_tools(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_tools(db, skip=skip, limit=limit)

@app.get("/tools/{tool_id}", response_model=schemas.Tool)
def read_tool(tool_id: int, db: Session = Depends(get_db)):
    tool = crud.get_tool(db, tool_id=tool_id)
    if tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")
    return tool

@app.put("/tools/{tool_id}", response_model=schemas.Tool)
def update_tool(tool_id: int, tool: schemas.ToolCreate, db: Session = Depends(get_db)):
    updated_tool = crud.update_tool(db, tool_id=tool_id, tool=tool)
    if updated_tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")
    return updated_tool

@app.delete("/tools/{tool_id}")
def delete_tool(tool_id: int, db: Session = Depends(get_db)):
    success = crud.delete_tool(db, tool_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tool not found")
    return {"message": "Tool deleted"}

@app.post("/tools/{tool_id}/borrow")
def borrow_tool(tool_id: int, borrower_name: str, db: Session = Depends(get_db)):
    tool = crud.borrow_tool(db, tool_id=tool_id, borrower_name=borrower_name)
    if tool is None:
        raise HTTPException(status_code=400, detail="Tool not available or not found")
    return tool

@app.post("/tools/{tool_id}/return")
def return_tool(tool_id: int, db: Session = Depends(get_db)):
    tool = crud.return_tool(db, tool_id=tool_id)
    if tool is None:
        raise HTTPException(status_code=400, detail="Tool not borrowed or not found")
    return tool

@app.get("/tools/available/", response_model=List[schemas.Tool])
def read_available_tools(db: Session = Depends(get_db)):
    return crud.get_available_tools(db)

@app.get("/tools/borrowed/", response_model=List[schemas.Tool])
def read_borrowed_tools(db: Session = Depends(get_db)):
    return crud.get_borrowed_tools(db)

@app.get("/tools/name/{name}", response_model=schemas.Tool)
def read_tool_by_name(name: str, db: Session = Depends(get_db)):
    tool = crud.get_tool_by_name(db, name=name)
    if tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")
    return tool
