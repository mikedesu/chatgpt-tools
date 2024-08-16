import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

model_list = client.models.list()

#print(model_list)

for d in model_list.data:
    print(d.id)

