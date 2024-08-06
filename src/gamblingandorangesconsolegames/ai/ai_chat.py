import os
import time
#import google.generativeai as genai

#genai.configure(api_key='redacted')

def clear_screen():
    
    os.system('cls' if os.name == 'nt' else 'clear')

def talk_to_ai():

    clear_screen()
    print("AI CHAT:")
    print("Hello! I'm an AI assistant powered by Gemini. How can I help you today?")
    print("Currently, I am not functioning properly, so please quit!")
    print("(Type 'quit' or 'exit' to return to the main menu)")
    
 #   model = genai.GenerativeModel('gemini-pro')
 #   chat = model.start_chat(history=[])
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ['quit', 'exit']:
            print("AI: Goodbye! Returning to main menu...")
            time.sleep(2)
            break
#        
#        try:
#            response = chat.send_message(user_input)
#            ai_response = response.text
#            print(f"AI: {ai_response}")
#        except Exception as e:
#            print(f"An error occurred: {e}")
 #           print("AI: I'm having trouble responding right now. Let's try again.")

if __name__ == "__main__":
    talk_to_ai()