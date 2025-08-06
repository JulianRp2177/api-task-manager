from pydantic import BaseModel, EmailStr


class AssignTask(BaseModel):
    user_email: EmailStr
