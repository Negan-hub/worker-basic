import runpod
import time
import base64
from PIL import Image, ImageDraw
from io import BytesIO

def generate_image(prompt):
    # 🧪 Dummy image generation for example
    img = Image.new('RGB', (512, 512), color=(73, 109, 137))
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), prompt, fill=(255, 255, 0))
    return img

def handler(event):
    print(f"Worker Start")
    input = event['input']
    
    prompt = input.get('prompt', 'No prompt provided')
    seconds = input.get('seconds', 0)

    print(f"Received prompt: {prompt}")
    print(f"Sleeping for {seconds} seconds...")
    time.sleep(seconds)

    # 🖼 Generate an image from the prompt
    img = generate_image(prompt)

    # 🔁 Convert the image to base64
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    # ✅ Return the base64 image
    return {
        "image": img_base64
    }

if __name__ == '__main__':
    runpod.serverless.start({'handler': handler})
