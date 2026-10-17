from pydantic import BaseModel


class UserResponse(BaseModel):
    uid: str
    email: str | None
    display_name: str | None
    onboarding_completed: bool
