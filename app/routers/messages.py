from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import get_current_user  # funcția care validează tokenul și extrage userul
from app.database import get_db
from app.dtos.AddMessageDto import AddMessageDto
from app.dtos.ResponseMessageLLMDto import ResponseMessageLLMDto
from app.dtos.SenderContentDto import SenderContentDto
from app.llm_utils.generate_response import generate_response_from_LLM
from app.services.messages import get_all_messages_by_conversation_id

router = APIRouter(
    prefix="/message",
    tags=["Messages"]
)

# Creare user nou
@router.post("/add_message", response_model=ResponseMessageLLMDto)
async def add_message(
    message_model:AddMessageDto,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)  # validare token Auth0
):
    response_from_LLM = await generate_response_from_LLM(message_model.sender)
    message = add_message(db, message_model.conversation_id, message_model.sender, response_from_LLM)
    return message

@router.get("/all_conversation/{conversation_id}", response_model=List[SenderContentDto])
def all_conversation(
        conversation_id:UUID,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)  # validare token Auth0

):
    return get_all_messages_by_conversation_id(db,conversation_id)