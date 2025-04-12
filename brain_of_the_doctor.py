# Step 1: Setup GROQ API Key
import os
from groq import Groq
from dotenv import load_dotenv
import base64
load_dotenv()

GROQ_API_KEY = os.environ['GROQ_API_KEY']
# Step 2: Convert image to base64 format

def encode_image(image_path):
    image_file = open(image_path, "rb") 
    return base64.b64encode(image_file.read()).decode('utf-8')

# Step 3: Setup multimodal LLM
model = "llama-3.2-90b-vision-preview"
query = "Is there something wrong with my face?"
def analyze_image_with_query(query, model, encoded_image):
    client = Groq(api_key=GROQ_API_KEY) 
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": query},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}",
                    },
                },
            ],
        }
    ]

    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model
    )

    return chat_completion.choices[0].message.content
