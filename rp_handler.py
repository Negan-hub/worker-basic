import runpod
import requests
import base64
import time

# API key
API_KEY = "rpa_M7MA3RHQV7WQ9T3BXXKJI6DAIXLSCEKNA4EM48DRcip67o"

# Model endpoint map
MODEL_ENDPOINTS = {
    "sd-1.5": "stable-diffusion-v1-5-bxswutwvm2l28s",
    "dreamshaper-v8": "dreamshaper-v8-bxswutwvm2l28s",
    "realistic-vision-v4": "realistic-vision-v4-bxswutwvm2l28s",
    "anything-v5": "anything-v5-bxswutwvm2l28s",
    "openjourney-v4": "openjourney-v4-bxswutwvm2l28s"
}

# Default model
DEFAULT_MODEL = "dreamshaper-v8"


def handler(event):
    print("Worker Start")
    input_data = event['input']

    prompt = input_data.get("prompt", "A futuristic cityscape at dusk")
    seconds = input_data.get("seconds", 0)
    model_key = input_data.get("model", DEFAULT_MODEL)

    # Sleep simulation
    print(f"Prompt: {prompt}")
    print(f"Model: {model_key}")
    print(f"Sleeping for {seconds} seconds...")
    time.sleep(seconds)

    # Resolve endpoint ID
    endpoint_id = MODEL_ENDPOINTS.get(model_key)
    if not endpoint_id:
        return {"error": f"Model '{model_key}' not found. Available: {list(MODEL_ENDPOINTS.keys())}"}

    # Send request to RunPod model
    print(f"Calling endpoint: {endpoint_id}")
    response = requests.post(
        f"https://api.runpod.ai/v2/{endpoint_id}/runsync",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"input": {"prompt": prompt}}
    )

    try:
        res_json = response.json()
        print("Response:", res_json)

        output = res_json.get("output")
        if isinstance(output, dict):
            image_url = output.get("image_url") or output.get("url")
        else:
            image_url = output

        if not image_url:
            raise Exception("No image URL returned from model.")

        # Download and encode image
        img_bytes = requests.get(image_url).content
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')

        return {
            "prompt": prompt,
            "model_used": model_key,
            "image_url": image_url,
            "image_base64": img_base64,
            "status": res_json.get("status"),
            "workerId": res_json.get("workerId")
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            "error": str(e),
            "response_text": response.text
        }


if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
