import time
import runpod
import requests
import os

def handler(event):
    print("🟢 Worker Started")
    input_data = event.get("input", {})
    env_vars = event.get("env", {})

    prompt = input_data.get("prompt", "a robot cat reading a book in the library")
    seconds = input_data.get("seconds", 0)

    print(f"📥 Received prompt: {prompt}")
    print(f"⏱ Sleeping for {seconds} seconds...")
    time.sleep(seconds)

    api_key = env_vars.get("RUNPOD_API_KEY") or os.getenv("RUNPOD_API_KEY")
    image_url = generate_image(prompt, api_key)

    return {
        "output": {
            "image_url": image_url
        }
    }

def generate_image(prompt, api_key):
    endpoint_id = "35y47vpnpgk9n9"
    run_url = f"https://api.runpod.ai/v2/{endpoint_id}/run"
    status_url_base = f"https://api.runpod.ai/v2/{endpoint_id}/status/"

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
        # Step 1: Submit job
        response = requests.post(run_url, headers=headers, json=payload)
        if response.status_code != 200:
            print(f"❌ Submit Error: {response.status_code} - {response.text}")
            return f"Error: HTTP {response.status_code} on job submission"
        
        job_data = response.json()
        job_id = job_data.get("id")
        if not job_id:
            print("❌ No job ID returned")
            return "Error: No job ID"

        print(f"📨 Job ID: {job_id}")

        # Step 2: Poll for completion
        for _ in range(30):  # Max wait ~30 x 3 = 90 seconds
            status_url = status_url_base + job_id
            status_resp = requests.get(status_url, headers=headers)
            status_data = status_resp.json()

            print(f"⏳ Job status: {status_data.get('status')}")
            if status_data.get("status") == "COMPLETED":
                output = status_data.get("output")
                if isinstance(output, dict) and "image_url" in output:
                    return output["image_url"]
                elif isinstance(output, list) and len(output) > 0:
                    return output[0].get("image", "No image found in list")
                else:
                    return "Error: Invalid output format"

            elif status_data.get("status") == "FAILED":
                return "Error: Job failed"

            time.sleep(3)  # wait before polling again

        return "Error: Job timeout"

    except Exception as e:
        print(f"❌ Exception: {e}")
        return f"Error: {str(e)}"

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
