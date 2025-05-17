from run_model import tokenizer, model_with_adapter


async def generate_response_from_LLM(user_message: str) -> str:
    alpaca_prompt = """Mai jos este o instrucțiune care descrie o sarcină. Scrie un răspuns care completează adecvat cererea.

    ### Instrucțiune:
    {}

    ### Răspuns:
    {}"""

    inputs = tokenizer(
        [alpaca_prompt.format(user_message, "")],
        return_tensors="pt"
    ).to("cuda")

    outputs = model_with_adapter.generate(**inputs, max_new_tokens=300, use_cache=True)
    result = tokenizer.decode(outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)

    raspuns = result.split('### Răspuns:')[1].strip()

    return raspuns