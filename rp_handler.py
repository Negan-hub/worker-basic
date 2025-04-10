import runpod
import time
import requests  # HTTP client for interacting with the image generation service

def handler(event):
    print(f"Worker Start")
    input_data = event['input']
    
    prompt = input_data.get('prompt')  # Get the text prompt for image generation
    seconds = input_data.get('seconds', 0)  # Optional delay for simulating processing time
    
    print(f"Received prompt: {prompt}")
    print(f"Sleeping for {seconds} seconds...")

    # Optional delay (simulate image generation processing time)
    time.sleep(seconds)

    # Call the image generation service
    image_url = generate_image(prompt)  # Replace with actual image generation logic
    
    # Return the generated image URL to the client
    return {
        "output": {
            "image_url": image_url  # The URL of the generated image or use base64 if needed
        }
    }

def generate_image(prompt):
    # Correct RunPod.io API URL for image generation (replace with the actual URL provided by RunPod.io)
    api_url = "https://api.runpod.ai/v2/tu66k591se3bqp/run"  # Example, replace with your actual endpoint
    
    # Headers for API authentication (use your provided API key)
    headers = {
        "Authorization": "Bearer rpa_M7MA3RHQV7WQ9T3BXXKJI6DAIXLSCEKNA4EM48DRcip67o"  # Your API key here
    }
    
    # Request payload
    data = {
        "prompt": prompt,      # The prompt for image generation
        "n": 1,                # Number of images to generate (usually 1)
        "size": "1024x1024"    # Image size (adjust based on RunPod's capabilities)
    }
    
    # Make the POST request to the image generation service
    response = requests.post(api_url, headers=headers, json=data)
    
    if response.status_code == 200:
        # Extract the URL of the generated image from the API response
        # The response structure depends on RunPod.io's specific API, this is an example
        image_url = response.json().get('image_url')
        if image_url:
            return image_url
        else:
            print("No image URL returned in the response.")
            return "https://fallback-image-url.com/default-image.png"  # Fallback image URL in case of error
    else:
        print(f"Error generating image: {response.status_code}")
        return "https://fallback-image-url.com/error-image.png"  # Fallback in case of API failure

if __name__ == '__main__':
    runpod.serverless.start({'handler': handler})
