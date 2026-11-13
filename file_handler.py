import os
from datetime import datetime

# Create folder if it does not exist
os.makedirs("chat_history", exist_ok=True)

def save_chat(user_message, bot_response):

    filename = "chat_history/conversation.txt"

    with open(filename, "a", encoding="utf-8") as file:

        file.write("\n" + "=" * 50 + "\n")

        file.write(
            f"Date: {datetime.now()}\n"
        )

        file.write(
            f"User: {user_message}\n"
        )

        file.write(
            f"Bot: {bot_response}\n"
        )