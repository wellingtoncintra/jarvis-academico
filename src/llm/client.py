from openai import OpenAI
import os
from dotenv import load_dotenv
 
load_dotenv()

client = OpenAI(base_url=os.getenv("LLM_BASE_URL"), api_key=os.getenv("LLM_API_KEY"))
resp = client.chat.completions.create(
    model=os.getenv("LLM_MODEL_NAME"),
    messages=[{'role': 'user', 'content': 'Hi'}],
)
print(resp.choices[0].message.content)