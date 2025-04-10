import runpod
import requests
import base64
from diffusers import StableDiffusionPipeline
import torch
from io import BytesIO
import base64

# Load the model
model = StableDiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-2-1",
    torch_dtype=torch.float16,
    variant="fp16",
    use_safetensors=True
)
model.to("cuda")

def handler(job):
    """
    This handler takes a text prompt and generates an image using Stable Diffusion.
    """
    job_input = job["input"]
    
    # Get the prompt from the input
    prompt = job_input.get("prompt", "A beautiful landscape")
    
    # Additional parameters (optional)
    num_inference_steps = job_input.get("num_inference_steps", 30)
    guidance_scale = job_input.get("guidance_scale", 7.5)
    
    # Generate the image
    image = model(
        prompt=prompt,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale,
    ).images[0]
    
    # Convert the image to base64
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    # Return the base64 encoded image
    return {
        "image": f"data:image/png;base64,{img_str}"
    }

# Start the serverless function
runpod.serverless.start({"handler": handler})
