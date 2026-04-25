from pydantic import BaseModel

class Player(BaseModel):
    name: str

class Score(BaseModel):
    player_id: int
    score: int

class User(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str
