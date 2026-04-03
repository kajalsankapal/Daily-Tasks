import os
from dotenv import load_dotenv
from google import genai

# -------- LOAD API KEY --------
load_dotenv()
client = genai.Client(api_key=os.getenv("gemini_api_key"))

# -------- SYSTEM PERSONA --------
SYSTEM_PROMPT = (
    "You are a professional Technical Recruiter. "
    "You ask interview questions, evaluate answers, and guide candidates. "
    "Never break character."
)

# -------- MEMORY --------
conversation_memory = []

# -------- FUNCTION TO GET RESPONSE --------
def get_response(user_input):
    global conversation_memory

    # Add user input
    conversation_memory.append(f"User: {user_input}")

    # -------- SLIDING WINDOW (last 5 exchanges = 10 messages) --------
    conversation_memory[:] = conversation_memory[-10:]

    # Combine everything into one context
    context = SYSTEM_PROMPT + "\n" + "\n".join(conversation_memory)

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=context
        )

        reply = response.text

        # Add bot reply to memory
        conversation_memory.append(f"Recruiter: {reply}")

        return reply

    except Exception as e:
        return f"Error: {e}"


# -------- CLI CHAT LOOP --------
print("👩‍💼 Technical Recruiter Chatbot (Gemini) - Type 'exit' to quit\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Good luck with your career! 🚀")
        break

    reply = get_response(user_input)
    print("Recruiter:", reply)