from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Simple in-memory database
users_db = {}

class User(BaseModel):
    id: int
    name: str
    email: str

# Create a new user
@app.post("/users/")
def create_user(user: User):
    if user.id in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[user.id] = user
    return {
        "message": "User created successfully",
        "user": user.dict()
    }


# Get user by ID
@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id in users_db:
        return users_db[user_id].dict()
    raise HTTPException(status_code=404, detail="User not found")

# Update user
@app.put("/users/{user_id}")
def update_user(user_id: int, updated_user: User):
    if user_id in users_db:
        users_db[user_id] = updated_user
        return {
            "message": "User updated successfully",
            "user": updated_user.dict()
        }
    raise HTTPException(status_code=404, detail="User not found")

# Delete user
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
    return {"message": "User deleted successfully"}
