from fastapi import FastAPI
from pydantic import BaseModel
from transformers import CLIPTextModel, CLIPTokenizer, DALL-E
import torch
from io import BytesIO
from PIL import Image
import base64

app = FastAPI()

# Load model
model_name = "dalle-mini"
tokenizer = CLIPTokenizer.from_pretrained(model_name)
model = CLIPTextModel.from_pretrained(model_name)

class TextInput(BaseModel):
    text: str

def generate_image_from_text(text: str):
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model.generate(**inputs)
    image = Image.open(BytesIO(outputs))  # Convert generated output to image format
    return image

@app.post("/generate_image/")
async def generate_image(text_input: TextInput):
    image = generate_image_from_text(text_input.text)
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return {"image_data": img_str}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
