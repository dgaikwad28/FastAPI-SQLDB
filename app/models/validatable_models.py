from pydantic import BaseModel, EmailStr, UUID4


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID4 = None
    username: str
    email: EmailStr
