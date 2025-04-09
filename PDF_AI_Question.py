import requests
from AI_Constants import api_url, headers

conversation_history = []  # Stores last 3 user inputs and AI responses
analyzed_pdf_data = None   # Store analyzed PDF data


def analyze_pdf(pdf_text):
  
    global analyzed_pdf_data
    analyzed_pdf_data = pdf_text  # Store PDF data
    print("PDF analyzed and stored.")


def generate_pdf_question(question):
    global conversation_history

    if analyzed_pdf_data is None:
        print("Error: No PDF has been analyzed yet.")
        return

    # Build conversation history 
    history_context = ""
    for exchange in conversation_history:
        history_context += f"USER: {exchange['user']}\nAI: {exchange['ai']}\n"

    # Prepare payload for API 
    payload = {
        "inputs": f"PDF CONTEXT: {analyzed_pdf_data}\n\nCONVERSATION HISTORY:\n{history_context}\nUSER QUESTION: {question}",
        "parameters": {
            "max_new_tokens": 150,
            "temperature": 0.5
        }
    }

    # Sending POST to API
    response = requests.post(api_url, headers=headers, json=payload)

    # Get AIs response
    if response.status_code == 200:
        ai_response = response.json()
        print(f"AI Response: {ai_response}")
    else:
        print(f"Error: API request failed with status code {response.status_code}")
        return

    # Update conversation history - only 3 entries
    conversation_history.append({"user": question, "ai": ai_response})
    if len(conversation_history) > 3:
        conversation_history.pop(0)  # Remove the oldest entry to keep only 3

    # Print  conversation history --- other
    # print("\nUpdated Conversation History (Last 3):")
    # for exchange in conversation_history:
    #     print(f"USER: {exchange['user']}")
    #     print(f"AI: {exchange['ai']}\n")


