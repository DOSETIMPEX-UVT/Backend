import uuid
from http.client import HTTPException

from sqlalchemy.orm import Session

from app.dtos.ConversationDto import ConversationDto
from app.models.Conversations import Conversation
from app.dtos.AddConversationDto import AddConversationDto
from app.models.Messages import Message


def get_conversations_by_user_id(db: Session, user_id: str) -> list[ConversationDto]:
    conversations = db.query(Conversation).filter(Conversation.user_id == user_id).all()
    return [ConversationDto.model_validate(conv) for conv in conversations]
def add_conversation_by_user_id(db:Session, add_model:AddConversationDto):
    db_conversation = Conversation(
        id=uuid.uuid4(),
        user_id=add_model.user_id,
        title=add_model.title,
    )
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return ConversationDto.model_validate(db_conversation)

def delete_conversation_by_user_id(db:Session, conversation_id):

    messages = db.query(Message).filter(Message.conversation_id == conversation_id).all()

    for message in messages:
        db.delete(message)

    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    db.delete(conversation)
    db.commit()

    return {"message": "Conversation and its messages deleted successfully."}