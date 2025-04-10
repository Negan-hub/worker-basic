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
    # Correct RunPod.io API URL format
    api_url = "https://api.runpod.ai/v2/jtbfmnx9lsehmo/runsync"  # Using runsync for synchronous response
    
    # Headers for API authentication
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer rpa_M7MA3RHQV7WQ9T3BXXKJI6DAIXLSCEKNA4EM48DRcip67o"
    }
    
    # Request payload in the correct format
    data = {
        "input": {
            "prompt": prompt
            # Add other parameters as needed based on your endpoint's requirements
        }
    }
    
    try:
        # Make the POST request to the image generation service
        response = requests.post(api_url, headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            
            if result["status"] == "COMPLETED":
                # The structure of output depends on your specific endpoint
                # For most image generation endpoints, it will be either a URL or base64 image
                if "output" in result and isinstance(result["output"], dict) and "image_url" in result["output"]:
                    return result["output"]["image_url"]
                elif "output" in result and isinstance(result["output"], list) and len(result["output"]) > 0:
                    # Some endpoints return a list of images
                    return result["output"][0].get("image", "No image URL found")
                else:
                    print(f"Unexpected response structure: {result}")
                    return "No image URL found in response"
            else:
                print(f"Job not completed: {result['status']}")
                return f"Error: Job status is {result['status']}"
        else:
            print(f"Error response: {response.status_code} - {response.text}")
            return f"Error: {response.status_code}"
    except Exception as e:
        print(f"Exception during image generation: {str(e)}")
        return f"Error: {str(e)}"
    
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
