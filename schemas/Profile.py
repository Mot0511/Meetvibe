from typing import Dict, List
from pydantic import BaseModel


class Profile(BaseModel):
    id: int
    user_id: int
    name: str
    age: int
    gender: str
    city: str
    location: Dict[str, float]
    school: str
    hobbies: List[str]
    description: str
    photo: str