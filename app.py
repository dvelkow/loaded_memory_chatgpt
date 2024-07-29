import os
import openai
from typing import List, Dict, Any

# IMPORTANT: Replace this with your actual API key or use an environment variable
OPENAI_API_KEY = "insert_key_here"

# Name of the knowledge base file in the same directory
KNOWLEDGE_BASE_FILE = "knowledge_base.txt"

def read_file(file_path: str) -> str:
    """Read the contents of a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def setup_openai_api() -> None:
    """Set up the OpenAI API key."""
    if OPENAI_API_KEY.startswith("sk-") and len(OPENAI_API_KEY) > 20:
        openai.api_key = OPENAI_API_KEY
    else:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            api_key = input("Please enter your OpenAI API key: ").strip()
            if not api_key:
                raise ValueError("API key is required to run this script.")
        os.environ['OPENAI_API_KEY'] = api_key
        openai.api_key = api_key

def create_messages(system_content: str, user_content: str) -> List[Dict[str, Any]]:
    """Create a list of messages for the OpenAI Chat API."""
    return [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content}
    ]

def get_ai_response(messages: List[Dict[str, Any]]) -> str:
    """Get a response from the OpenAI Chat API using GPT-4."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-0125-preview",  # This is the GPT-4 Turbo model
            messages=messages
        )
        return response.choices[0].message['content'].strip()
    except openai.error.AuthenticationError:
        print("Authentication error: Your API key may be invalid or expired.")
        return "I'm sorry, there was an authentication error. Please check your API key."
    except openai.error.RateLimitError:
        print("Rate limit exceeded: Please try again later.")
        return "I'm sorry, the rate limit has been exceeded. Please try again later."
    except Exception as e:
        print(f"An error occurred: {e}")
        return "I'm sorry, I encountered an error while processing your request."

def chatbot(knowledge_base: str) -> None:
    """Run the chatbot."""
    system_message = f"""You are a helpful assistant. Your knowledge comes from the following text:

{knowledge_base}

If you don't find relevant information in your knowledge base to answer a question, respond with "I have no info about that." Always strive to provide accurate information based on your knowledge base."""

    print("Chatbot: Hello! I'm ready to answer your questions based on my knowledge base. Type 'quit' to exit.")

    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == 'quit':
            print("Chatbot: Goodbye!")
            break

        messages = create_messages(system_message, user_input)
        ai_response = get_ai_response(messages)
        print(f"Chatbot: {ai_response}")

def main() -> None:
    """Main function to run the program."""
    try:
        setup_openai_api()
        
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the full path to the knowledge base file
        knowledge_base_path = os.path.join(script_dir, KNOWLEDGE_BASE_FILE)
        
        if not os.path.exists(knowledge_base_path):
            raise FileNotFoundError(f"The file {KNOWLEDGE_BASE_FILE} does not exist in the script directory.")
        
        knowledge_base = read_file(knowledge_base_path)
        
        chatbot(knowledge_base)
    except ValueError as ve:
        print(f"Error: {ve}")
    except FileNotFoundError as fnf:
        print(f"Error: {fnf}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()