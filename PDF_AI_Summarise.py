import requests
from AI_Constants import api_url, headers

def generate_pdf_summary(pdf_text):
    max_input_length = 6000
    truncated_text = pdf_text[:max_input_length]
    
    prompt = """<system>
You are a professional document summarizer. You create concise and accurate text summaries.
</system>

<user>
Summarize the following text in 2-4 sentences. Focus on main themes only. Create a paragraph, not bullet points.
Don't include dates, URLs or contact details. Write in third person.

TEXT:
{}
</user>

<assistant>""".format(truncated_text)
    
    payload = {   
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 150,
            "temperature": 0.1,
            "top_p": 0.85,
            "do_sample": True       
        }
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response_json = response.json()
        
        print("API Response Status:", response.status_code)
        print("API Response Structure:", type(response_json))
        
        if response.status_code == 200:
            generated_text = None
            
            if isinstance(response_json, list) and len(response_json) > 0:
                if isinstance(response_json[0], dict) and 'generated_text' in response_json[0]:
                    generated_text = response_json[0]['generated_text']
            elif isinstance(response_json, dict) and 'generated_text' in response_json:
                generated_text = response_json['generated_text']
                
            if generated_text:
                if "<assistant>" in generated_text:
                    summary = generated_text.split("<assistant>")[-1].strip()
                    return summary
                else:
                    clean_text = generated_text
                    
                    markers = ["<system>", "<user>", "TEXT:", "Summarize the following"]
                    
                    for marker in markers:
                        if marker in clean_text:
                            parts = clean_text.split(marker)
                            if len(parts) > 1:
                                clean_text = parts[-1].strip()
                    
                    return clean_text
            
            return str(response_json)
        else:
            return f"API Error: {response.status_code}\n{response.text}"
    except Exception as e:
        return f"Error generating summary: {str(e)}"

