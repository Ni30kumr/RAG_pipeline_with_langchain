# from fastapi import FastAPI, Depends, HTTPException, status,Query
# from fastapi import File, UploadFile
# import shutil
# import os
# from database import engine,Base,SessionLocal
# from sqlalchemy.orm import Session
# from pydantic import BaseModel
# from models import User
# from lang_data import create_user_index,hf,pc
# from query import get_user_rag_chain
# import json
# from sqlalchemy import or_
# from typing import List
# from langchain_pinecone import PineconeVectorStore

# Base.metadata.create_all(bind=engine)

# app = FastAPI()

# class DeleteUserRequest(BaseModel):
#     username: str
#     password: str
#     user_id: int

# # Dependency to get database session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# class UserCreate(BaseModel):
#     username: str
#     email: str
#     password: str

# class UserResponse(BaseModel):
#     id: int
#     username: str
#     email: str
    
# class UserOut(BaseModel):
#     id: int
#     username: str
#     email: str
#     bot_config: str | None

#     class Config:
#         from_attributes = True

# # User registration endpoint
# @app.post("/users/", response_model=UserResponse)
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     db_user = User(username=user.username, email=user.email, hashed_password=user.password)  # In real app, hash the password
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


# @app.post("/users/{user_id}/setup_bot")
# async def setup_user_bot(
#     user_id: int, 
#     file: UploadFile = File(...), 
#     db: Session = Depends(get_db)
# ):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     # Create a directory for the user if it doesn't exist
#     user_dir = f"user_files/{user.username}"
#     os.makedirs(user_dir, exist_ok=True)
    
#     # Save the uploaded file
#     file_path = f"{user_dir}/{file.filename}"
#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
#     print(file_path)
    
#     # Create the user's index and load documents
#     docsearch = create_user_index(user.username, file_path)
    
#     # Store the configuration
#     user.bot_config = json.dumps({
#         "pdf_path": file_path,
#         "index_name": f"user-{user.username}-index"
#     })
#     db.commit()
    
#     return {"message": "Bot setup complete", "file_path": file_path}

# @app.post("/users/{user_id}/query")
# def query_user_bot(user_id: int, query: str, db: Session = Depends(get_db)):
#     print(query)
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     if not user.bot_config:
#         raise HTTPException(status_code=400, detail="Bot not set up for this user")
    
#     config = json.loads(user.bot_config)
    
#     # Retrieve the existing index
#     index = config["index_name"]
#     docsearch = PineconeVectorStore(index_name=index,embedding=hf)
    
#     # Get the RAG chain
#     rag_chain = get_user_rag_chain(docsearch)
    
#     # Query the bot
#     result = rag_chain.invoke(query)
#     return {"answer": result}



# @app.get("/users/search", response_model=List[UserOut])
# def search_users(
#     username: str | None = Query(None, min_length=3),
#     email: str | None = Query(None, min_length=3),
#     db: Session = Depends(get_db)
# ):
#     if not username and not email:
#         raise HTTPException(status_code=400, detail="Please provide either username or email")
    
#     query = db.query(User)
    
#     if username:
#         query = query.filter(User.username.ilike(f"%{username}%"))
    
#     if email:
#         query = query.filter(User.email.ilike(f"%{email}%"))
    
#     users = query.all()
    
#     if not users:
#         raise HTTPException(status_code=404, detail="No users found")
    
#     return users


# @app.post("/users/delete")
# def delete_user(
#     delete_request: DeleteUserRequest,
#     db: Session = Depends(get_db)
# ):
#     # Fetch the user
#     user = db.query(User).filter(User.id == delete_request.user_id).first()
    
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     # Verify username and password
#     if user.username != delete_request.username or user.hashed_password != delete_request.password:
#         raise HTTPException(status_code=401, detail="Invalid credentials")
    
#     # Delete Pinecone index if it exists
#     if user.bot_config:
#         config = json.loads(user.bot_config)
#         index_name = config["index_name"]
#         if index_name:
#             try:
#                 pc.delete_index(index_name)
#             except Exception as e:
#                 print(f"Error deleting Pinecone index: {e}")
#                 # Optionally, you might want to raise an HTTPException here
    
#     # Delete user from MySQL
#     db.delete(user)
#     db.commit()
    
#     return {"message": "User and associated data deleted successfully"}















from fastapi import FastAPI, Depends, File, UploadFile, Query
from database import engine, Base, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from user_manager import UserManager

Base.metadata.create_all(bind=engine)

app = FastAPI()

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    
class UserOut(BaseModel):
    id: int
    username: str
    email: str
    bot_config: str | None

    class Config:
        from_attributes = True

class DeleteUserRequest(BaseModel):
    username: str
    password: str
    user_id: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return UserManager.create_user(user, db)

@app.post("/users/{user_id}/setup_bot")
async def setup_user_bot(user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    return UserManager.setup_bot(user_id, file, db)

@app.post("/users/{user_id}/query")
def query_user_bot(user_id: int, query: str, db: Session = Depends(get_db)):
    return UserManager.query_bot(user_id, query, db)

@app.get("/users/search", response_model=List[UserOut])
def search_users(
    username: str | None = Query(None, min_length=3),
    email: str | None = Query(None, min_length=3),
    db: Session = Depends(get_db)
):
    return UserManager.search_users(username, email, db)

@app.post("/users/delete")
def delete_user(delete_request: DeleteUserRequest, db: Session = Depends(get_db)):
    return UserManager.delete_user(delete_request, db)