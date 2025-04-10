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
    endpoint_id = "jtbfmnx9lsehmo"
    api_url = f"https://api.runpod.ai/v2/cefewmzuxzvft1/run"
    status_url = f"https://api.runpod.ai/v2/cefewmzuxzvft1/status"
    api_key = os.getenv("RUNPOD_API_KEY")

    if not api_key:
        print("API key is missing. Set RUNPOD_API_KEY in the environment.")
        return "Error: API key missing"

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
        # Step 1: Submit the job
        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code != 200:
            print(f"Failed to submit job: {response.status_code} - {response.text}")
            return f"Error: {response.status_code}"

        job_id = response.json().get("id")
        if not job_id:
            print("No job ID returned from RunPod")
            return "Error: No job ID"

        print(f"Job submitted. ID: {job_id}")

        # Step 2: Poll for job completion
        for attempt in range(20):  # Poll for up to ~60 seconds (20 * 3s)
            time.sleep(3)
            poll_response = requests.get(f"{status_url}/{job_id}", headers=headers)

            if poll_response.status_code != 200:
                print(f"Polling failed: {poll_response.status_code} - {poll_response.text}")
                continue

            result = poll_response.json()
            status = result.get("status")

            print(f"Polling attempt {attempt+1}: status = {status}")

            if status == "COMPLETED":
                output = result.get("output")
                if isinstance(output, dict) and "image_url" in output:
                    return output["image_url"]
                elif isinstance(output, list) and len(output) > 0:
                    return output[0].get("image", "No image URL found")
                else:
                    return "Error: Unexpected output format"
            elif status == "FAILED":
                return "Error: Job failed"

        return "Error: Job did not complete in time"

    except Exception as e:
        print(f"Exception during image generation: {e}")
        return f"Error: {str(e)}"

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
