import requests
import base64
import io
from PIL import Image

url = 'https://api.runpod.ai/v2/klnlbtwd3gjb0l/run.proxy.runpod.net/runsync'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}
data = {
    'input': {
        'prompt': "A detailed scene of a cyberpunk cat riding a motorcycle through a neon-lit Tokyo street at night"
    }
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    result = response.json()

    if result['status'] == 'COMPLETED':
        base64_image = result['output']

        # Remove the data URI prefix
        base64_string = base64_image.split(',')[1]

        # Decode the base64 string
        image_data = base64.b64decode(base64_string)

        # Create an image object from the decoded data
        image = Image.open(io.BytesIO(image_data))

        # Save the image as a PNG file
        image.save('output_image.png', 'PNG')

        print("Image saved as 'output_image.png'")

    else:
        print(f"Request status: {result['status']}")
else:
    print(f"Request failed with status code: {response.status_code}")