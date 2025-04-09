import requests
from AI_Constants import api_url, headers

def generate_pdf_summary(pdf_text):
    payload = {   
        "inputs": f"CREATE A SUMMARY OF THE FOLLOWING PDF TEXT: \n\n{pdf_text}",
        "parameters": {
            "max_new_tokens": 150,
            "temperature": 0.5
        }
    }

    # Sending the POST request to the Inference API
    response = requests.post(api_url, headers=headers, json=payload)

    # Print the generated output
    print(response.json())

