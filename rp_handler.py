import runpod
import requests
import time

# Replace with your actual RunPod API key and endpoint ID
API_KEY = "rpa_M7MA3RHQV7WQ9T3BXXKJI6DAIXLSCEKNA4EM48DRcip67o"
ENDPOINT_ID = "<your-stable-diffusion-endpoint-id>"

def handler(event):
    print("Worker Start")
    input = event['input']

    prompt = input.get('prompt')
    seconds = input.get('seconds', 0)

    print(f"Received prompt: {prompt}")
    print(f"Sleeping for {seconds} seconds...")

    time.sleep(seconds)

    # Send request to the text-to-image endpoint
    response = requests.post(
        f"https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"input": {"prompt": prompt}}
    )

    if response.status_code == 200:
        image_url = response.json().get('output')
        return {"prompt": prompt, "image_url": image_url}
    else:
        return {"error": response.text}
    
if __name__ == '__main__':
    runpod.serverless.start({'handler': handler})
