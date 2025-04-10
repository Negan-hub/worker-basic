import runpod
import time
import base64
from PIL import Image, ImageDraw
from io import BytesIO

def generate_image(prompt):
    # Dummy image with prompt text for demonstration
    img = Image.new('RGB', (512, 512), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    draw.text((20, 250), prompt[:40], fill=(255, 255, 0))  # Draw prompt text
    return img

def handler(event):
    print("Worker Start")
    input = event['input']
    
    prompt = input.get('prompt', 'No prompt provided')
    seconds = input.get('seconds', 0)

    print(f"Received prompt: {prompt}")
    time.sleep(seconds)

    # Generate dummy image
    img = generate_image(prompt)

    # Convert image to base64
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # Return base64 image in output
    return {
        "image": img_base64
    }

if __name__ == '__main__':
    runpod.serverless.start({'handler': handler})
