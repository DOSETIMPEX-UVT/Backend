from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.auth import get_current_user  # funcția care validează tokenul și extrage userul
from app.database import get_db
from app.dtos.AddConversationDto import AddConversationDto
from app.dtos.ConversationDto import ConversationDto
from app.dtos.ResponseMessageLLMDto import ResponseMessageLLMDto
from app.llm_utils.generate_response import generate_response_from_LLM
from app.models.Conversations import Conversation
from app.services.conversations import get_conversations_by_user_id, add_conversation_by_user_id
from app.services.messages import add_message

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"]
)

@router.get("/all_conversations/{user_id}", response_model=List[ConversationDto])
def get_all_conversations(user_id: str,
                          db: Session = Depends(get_db),
                          current_user: dict = Depends(get_current_user)  # validare token Auth0
                          ):
    return get_conversations_by_user_id(db, user_id)


@router.post("/add_conversation", response_model=ResponseMessageLLMDto)
async def add_conversation(add_model:AddConversationDto,
                     db:Session = Depends(get_db),
                     current_user: dict = Depends(get_current_user)  # validare token Auth0
                     ):
    conversation_dto = add_conversation_by_user_id(db, add_model)
    response_from_LLM = await generate_response_from_LLM(add_model.sender)
    message = add_message(db, conversation_dto.id, add_model.sender, response_from_LLM)
    return message


