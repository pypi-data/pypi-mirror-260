from pydantic import BaseModel, Field


class FirebaseNotification(BaseModel):
    title: str = Field()
    body: str = Field()
