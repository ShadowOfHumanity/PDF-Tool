import requests


# MODEL
model_id = "EleutherAI/gpt-neo-2.7B"

# TOKEN
api_token = "" # Insert your token here but never commit it

# API endpoint URL
api_url = f"https://api-inference.huggingface.co/models/{model_id}"

# Headers, including your API token
headers = {
    "Authorization": f"Bearer {api_token}"
}

# Input payload for text generation (customize 'inputs' as needed)
payload = {
    "inputs": "Once upon a time in a land far, far away,",
    "parameters": {
        "max_new_tokens": 50,
        "temperature": 0.7
    }
}

# Sending the POST request to the Inference API
response = requests.post(api_url, headers=headers, json=payload)

# Print the generated output
print(response.json())
