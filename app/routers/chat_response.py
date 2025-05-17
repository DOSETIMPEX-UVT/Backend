from app.llm_utils.generate_response_from_LLM import generate_response_from_LLM
from fastapi import APIRouter

router = APIRouter()

@router.post("/chat_response")
async def test_llm_endpoint(data: dict):
    user_message = data.get("message")
    if not user_message:
        return {"error": "Mesajul este obligatoriu."}
    response = await generate_response_from_LLM(user_message)
    print("LLM Response:", response)
    return {"response": response}
