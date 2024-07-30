# user_manager.py

from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import User
from lang_data import create_user_index, hf, pc
from query import get_user_rag_chain
from langchain_pinecone import PineconeVectorStore
import json
import os
import shutil

class UserManager:
    @staticmethod
    def create_user(user, db: Session):
        db_user = User(username=user.username, email=user.email, hashed_password=user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def setup_bot(user_id: int, file, db: Session):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user_dir = f"user_files/{user.username}"
        os.makedirs(user_dir, exist_ok=True)
        
        file_path = f"{user_dir}/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        docsearch = create_user_index(user.username, file_path)
        
        user.bot_config = json.dumps({
            "pdf_path": file_path,
            "index_name": f"user-{user.username}-index"
        })
        db.commit()
        
        return {"message": "Bot setup complete", "file_path": file_path}

    @staticmethod
    def query_bot(user_id: int, query: str, db: Session):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if not user.bot_config:
            raise HTTPException(status_code=400, detail="Bot not set up for this user")
        
        config = json.loads(user.bot_config)
        
        index = config["index_name"]
        docsearch = PineconeVectorStore(index_name=index, embedding=hf)
        
        rag_chain = get_user_rag_chain(docsearch)
        
        result = rag_chain.invoke(query)
        return {"answer": result}

    @staticmethod
    def search_users(username: str | None, email: str | None, db: Session):
        if not username and not email:
            raise HTTPException(status_code=400, detail="Please provide either username or email")
        
        query = db.query(User)
        
        if username:
            query = query.filter(User.username.ilike(f"%{username}%"))
        
        if email:
            query = query.filter(User.email.ilike(f"%{email}%"))
        
        users = query.all()
        
        if not users:
            raise HTTPException(status_code=404, detail="No users found")
        
        return users

    @staticmethod
    def delete_user(delete_request, db: Session):
        user = db.query(User).filter(User.id == delete_request.user_id).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if user.username != delete_request.username or user.hashed_password != delete_request.password:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        if user.bot_config:
            config = json.loads(user.bot_config)
            index_name = config["index_name"]
            if index_name:
                try:
                    pc.delete_index(index_name)
                except Exception as e:
                    print(f"Error deleting Pinecone index: {e}")
        
        db.delete(user)
        db.commit()
        
        return {"message": "User and associated data deleted successfully"}