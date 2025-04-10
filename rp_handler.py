import time
import runpod
import requests
import os

def handler(event):
    print("🟢 Worker Started")
    input_data = event.get("input", {})
    env_vars = event.get("env", {})

    # Prompt and optional delay
    prompt = input_data.get("prompt", "a cat in a space suit on Mars")
    seconds = input_data.get("seconds", 0)

    print(f"📥 Received prompt: {prompt}")
    print(f"⏱ Sleeping for {seconds} seconds...")
    time.sleep(seconds)

    # Get API key from environment variable
    api_key = env_vars.get("RUNPOD_API_KEY") or os.getenv("RUNPOD_API_KEY")

    # Generate the image
    image_url = generate_image(prompt, api_key)

    return {
        "output": {
            "image_url": image_url
        }
    }

def generate_image(prompt, api_key):
    # Set your actual RunPod endpoint ID here
    endpoint_id = "35y47vpnpgk9n9"
    api_url = f"https://api.runpod.ai/v2/z15jet1uh56jvp/runsync"

    if not api_key:
        print("❌ Error: RUNPOD_API_KEY is not set.")
        return "Error: API key missing"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "input": {
            "prompt": prompt
        }
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        print(f"🔁 Response Status: {response.status_code}")
        print(f"📨 Response Text: {response.text}")
        result = response.json()

        if response.status_code != 200:
            return f"Error: HTTP {response.status_code}"

        status = result.get("status")
        output = result.get("output")

        if status != "COMPLETED":
            print(f"⚠️ Job not completed: status = {status}")
            return f"Error: Job status {status}"

        # Handle various output formats
        if isinstance(output, dict) and "image_url" in output:
            return output["image_url"]
        elif isinstance(output, list) and len(output) > 0:
            return output[0].get("image", "No image found in list")
        else:
            print(f"⚠️ Unexpected output format: {output}")
            return "Error: Invalid output format"

    except Exception as e:
        print(f"❌ Exception during image generation: {e}")
        return f"Error: {str(e)}"

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
