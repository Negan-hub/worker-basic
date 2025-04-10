import runpod
import requests
import time
import base64

# Your RunPod API key and endpoint ID
API_KEY = "rpa_M7MA3RHQV7WQ9T3BXXKJI6DAIXLSCEKNA4EM48DRcip67o"
ENDPOINT_ID = "https://api.runpod.ai/v2/bxswutwvm2l28s/run"

def handler(event):
    print("Worker Start")
    input = event['input']

    prompt = input.get('prompt')
    seconds = input.get('seconds', 0)

    print(f"Received prompt: {prompt}")
    print(f"Sleeping for {seconds} seconds...")
    time.sleep(seconds)

    # Send the prompt to the RunPod endpoint (sync)
    response = requests.post(
        f"https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"input": {"prompt": prompt}}
    )

    try:
        res_json = response.json()
        print("Full response:", res_json)

        # Extract image URL from response
        output = res_json.get("output")
        if isinstance(output, dict):
            image_url = output.get("image_url") or output.get("url")
        else:
            image_url = output  # if it's a plain string

        # Fetch image content
        image_response = requests.get(image_url)
        image_bytes = image_response.content

        # Encode image to base64
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')

        return {
            "prompt": prompt,
            "image_url": image_url,
            "image_base64": image_base64,
            "status": res_json.get("status"),
            "workerId": res_json.get("workerId")
        }

    except Exception as e:
        print("Error:", e)
        return {"error": str(e), "raw_response": response.text}


if __name__ == '__main__':
    runpod.serverless.start({'handler': handler})
