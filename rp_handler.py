import runpod
import base64
import io
from PIL import Image
from diffusers import StableDiffusionPipeline
import torch

def handler(event):
    print(f"Worker Start")
    input_data = event['input']
    
    prompt = input_data.get('prompt', "A beautiful landscape")
    
    print(f"Received prompt: {prompt}")
    
    # Load the model
    pipe = StableDiffusionPipeline.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.float16)
    pipe = pipe.to("cuda")
    
    # Generate the image
    image = pipe(prompt).images[0]
    
    # Convert image to base64 for returning
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    # Return the base64 encoded image
    return f"data:image/png;base64,{img_str}"

if __name__ == '__main__':
    runpod.serverless.start({'handler': handler})
