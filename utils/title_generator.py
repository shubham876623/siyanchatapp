import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_type = "azure"
openai.api_key = os.getenv("AZURE_API_KEY")
openai.api_base = os.getenv("AZURE_API_BASE")
openai.api_version = os.getenv("AZURE_API_VERSION")
deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME")

def generate_title(prompt):
    try:
        system_prompt = "You are a helpful assistant that summarizes user prompts into short, clear titles (3-5 words)."
        response = openai.ChatCompletion.create(
            engine=deployment_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Generate a short title: {prompt}"}
            ]
        )
        return response['choices'][0]['message']['content'].strip().title()
    except:
        return "Untitled Chat"
