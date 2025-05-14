import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_type = "azure"
openai.api_key = os.getenv("AZURE_API_KEY")
openai.api_base = os.getenv("AZURE_API_BASE")
openai.api_version = os.getenv("AZURE_API_VERSION")
engine = os.getenv("AZURE_DEPLOYMENT_NAME")

def get_gpt_response(question, context_chunks, mode, system_prompt):
    context = "\n\n".join(context_chunks) if context_chunks else ""

    if mode == "Docs only":
        prompt = f"Use the following psychiatry notes to answer the question.\n\nContext:\n{context}\n\nQuestion: {question}"
    elif mode == "Hybrid (GPT + Docs)":
        prompt = f"Use both your medical knowledge and the following private notes to answer.\n\nContext:\n{context}\n\nQuestion: {question}"
    else:
        prompt = question

    # Build conversation from history plus new user input
    from streamlit import session_state as state
    messages = [{"role": "system", "content": system_prompt}]
    for role, msg in state.chat_history:
        messages.append({"role": role, "content": msg})
    messages.append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(
        engine=engine,
        messages=messages
    )
    return response['choices'][0]['message']['content']
