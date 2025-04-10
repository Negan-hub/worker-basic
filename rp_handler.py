import runpod
import requests
import time
import base64

# RunPod API Key and Endpoint
API_KEY = "rpa_M7MA3RHQV7WQ9T3BXXKJI6DAIXLSCEKNA4EM48DRcip67o"
ENDPOINT_ID = "https://api.runpod.ai/v2/bxswutwvm2l28s/run"  # <-- must be a running image-gen endpoint

def handler(event):
    print("Worker Start")
    input_data = event['input']

    prompt = input_data.get('prompt')
    seconds = input_data.get('seconds', 0)

    print(f"Prompt: {prompt}")
    print(f"Sleeping for {seconds} seconds...")
    time.sleep(seconds)

    # --- Call the image generation endpoint (sync)
    print("Sending request to text-to-image endpoint...")
    response = requests.post(
        f"https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"input": {"prompt": prompt}}
    )

    # --- Check the result
    try:
        res_json = response.json()
        print("Full response from image endpoint:", res_json)

        output = res_json.get("output")

        # Try to get image URL from 'output'
        if isinstance(output, dict):
            image_url = output.get("image_url") or output.get("url")
        else:
            image_url = output

        if not image_url:
            raise Exception("No image URL returned from endpoint.")

        # --- Fetch the image and convert to base64
        image_response = requests.get(image_url)
        image_bytes = image_response.content
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')

        return {
            "prompt": prompt,
            "image_url": image_url,
            "image_base64": image_base64,
            "status": res_json.get("status"),
            "workerId": res_json.get("workerId")
        }

    except Exception as e:
        print("Error occurred:", str(e))
        return {
            "error": str(e),
            "response_text": response.text
        }

if __name__ == '__main__':
    runpod.serverless.start({'handler': handler})
