import os
import time
import runpod
import requests

def handler(event):
    print("Worker Start")
    input_data = event['input']
    
    prompt = input_data.get('prompt')
    seconds = input_data.get('seconds', 0)
    
    print(f"Received prompt: {prompt}")
    print(f"Sleeping for {seconds} seconds...")
    time.sleep(seconds)

    image_url = generate_image(prompt)

    return {
        "output": {
            "image_url": image_url
        }
    }

def generate_image(prompt):
    api_url = "https://api.runpod.ai/v2/jtbfmnx9lsehmo/runsync"
    api_key = "rpa_M7MA3RHQV7WQ9T3BXXKJI6DAIXLSCEKNA4EM48DRcip67o"  # Replace with your actual API key
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "input": {
            "prompt": prompt
        }
    }

    try:
        response = requests.post(api_url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()

            if result.get("status") == "COMPLETED":
                output = result.get("output")
                if isinstance(output, dict) and "image_url" in output:
                    return output["image_url"]
                elif isinstance(output, list) and len(output) > 0:
                    return output[0].get("image", "No image URL found")
                else:
                    print("Unexpected response format.")
                    return "Error: Invalid output format"
            else:
                return f"Error: Job status {result.get('status')}"
        else:
            print(f"HTTP error: {response.status_code} - {response.text}")
            return f"Error: HTTP {response.status_code}"
    except Exception as e:
        print(f"Exception during image generation: {e}")
        return f"Error: {str(e)}"

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
