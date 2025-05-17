from typing import List
from uuid import UUID
from fastapi import UploadFile, File
import os, tempfile, sys
from subprocess import run
from fastapi.responses import JSONResponse
from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.messages import add_message
from uuid import UUID

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

# Adaugare document .docx
@router.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename)[-1].lower()
    if suffix != ".docx":
        return JSONResponse(content={"error": "Se acceptă doar fișiere .docx."}, status_code=400)

    try:
        raw_name = file.filename.strip().lower().replace(" ", "_")
        os.makedirs("storage/temp_files", exist_ok=True)
        raw_path = os.path.join("storage/temp_files", raw_name)

        with open(raw_path, "wb") as f:
            f.write(await file.read())

        run([sys.executable, "upload_processing/process_uploaded_file.py", raw_name])

        processed_path = os.path.join("storage/processed", raw_name.replace(suffix, ".txt"))
        if not os.path.exists(processed_path):
            return JSONResponse(content={"error": "Textul nu a fost extras corect."}, status_code=400)

        with open(processed_path, "r", encoding="utf-8") as f:
            content = f.read()

        return {"extractedText": content[:2000]}

    except Exception as e:
        import traceback
        print("Eroare la upload:", traceback.format_exc())
        return JSONResponse(content={"error": str(e)}, status_code=500)



@router.get("/all_conversation/{conversation_id}", response_model=List[SenderContentDto])
def all_conversation(
        conversation_id:UUID,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)  # validare token Auth0

):
    return get_all_messages_by_conversation_id(db,conversation_id)
