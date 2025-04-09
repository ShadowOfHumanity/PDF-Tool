# MODEL
model_id = "EleutherAI/gpt-neo-2.7B"

# TOKEN
api_token = "" # Insert your token here but never commit it! imp

# API endpoint URL
api_url = f"https://api-inference.huggingface.co/models/{model_id}"

# Headers, including your API token
headers = {
    "Authorization": f"Bearer {api_token}"
}