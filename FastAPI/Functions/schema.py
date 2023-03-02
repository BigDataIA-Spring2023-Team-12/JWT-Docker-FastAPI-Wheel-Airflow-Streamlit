from pydantic import BaseModel


# schema for login
class LoginDetails(BaseModel):
    username: str
    password: str


# schema for user registration
class RegisterDetails(BaseModel):
    name: str
    plan: str
    username: str
    password: str

class ChangePasswordDetails(BaseModel):
    username: str
    current_password: str
    new_password: str
