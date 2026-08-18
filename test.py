import os
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI

load_dotenv()

key = os.getenv("MISTRAL_API_KEY")

print("Key exists:", key is not None)
print("Key length:", len(key) if key else 0)

llm = ChatMistralAI(
    model="mistral-small-latest",
    api_key=key,
    temperature=0
)

response = llm.invoke("Say hello")

print(response.content)