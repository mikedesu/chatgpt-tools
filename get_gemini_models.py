from openai import OpenAI
import os

client = OpenAI(
    # api_key="GEMINI_API_KEY",
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

models = client.models.list()
for model in models:
    print(model.id)
