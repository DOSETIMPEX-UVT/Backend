from uuid import UUID

from pydantic import BaseModel

class AddConversationDto(BaseModel):
        user_id: str
        title: str
        sender: str

        class Config:
                from_attributes = True
