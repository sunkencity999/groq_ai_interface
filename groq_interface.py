#!/usr/bin/env python3

from dotenv import load_dotenv
import os
import pyperclip
import logging
from groq import Groq
import datetime  # Added this module for using datetime

load_dotenv()

# Constants
ANSWERS_DIR = 'answers'

# Setup logging
logging.basicConfig(level=logging.INFO)

def call_groq_ai(client, question):
    """Calls the Groq AI API and returns the response."""
    try:
        chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": question}],
            model="llama-3.1-70b-versatile",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        logging.error(f"Error during API call ({type(e).__name__}): {e}")
        return None

def save_answer(answer, timestamp):
    """Saves the given answer to a file."""
    os.makedirs(ANSWERS_DIR, exist_ok=True)  # Create 'answers' directory if it doesn't exist
    filename = f"{timestamp}.txt"
    with open(os.path.join(ANSWERS_DIR, filename), 'a') as f:
        f.write(answer + '\\n')  # Ensure newline character is properly formatted
    logging.info(f"Answer saved to {filename}")

def main():
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    print("Welcome to the Groq AI interface!")

    while True:
        question = input("\n Please enter your question: ").strip()

        if not question:
            print("Question cannot be empty. Please ask something.")
            continue

        # Call the Groq AI API
        answer = call_groq_ai(client, question)
        if answer is None:
            continue  # If there's an error, ask for a new question

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        print(f"\n Groq AI says: {answer}")

        save_choice = input("Would you like to save or copy this output? (save/copy/none): ").strip().lower()
        if save_choice == 'save':
            save_answer(answer, timestamp)
        elif save_choice == 'copy':
    
            print("Here is an easy to copy display of the answer:") 
            print(answer)

        # Ask if the user wants to continue
        continue_choice = input("Would you like to ask another question? (yes/no): ").strip().lower()
        if continue_choice != 'yes':
            print("Thank you for using the Groq AI interface. Goodbye!")
            break

if __name__ == "__main__":
    main()
