import os

def think(user_input):
    """
    JARVIS brain - user input ki smart reply isthundi.
    Free mode: rule-based smart replies (API key అక్కర్లేదు).
    Later: Claude/GPT API connect cheyyadam.
    """
    user_input = user_input.lower().strip()

    # --- Time / Date ---
    if any(word in user_input for word in ["time", "what time", "time enti"]):
        import datetime
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"Current time is {now} boss."

    if any(word in user_input for word in ["date", "today", "entha tariku"]):
        import datetime
        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        return f"Today is {today}."

    # --- Greetings ---
    if any(word in user_input for word in ["hello", "hi", "hey", "jarvis"]):
        return "Hello boss! How can I help you today?"

    if any(word in user_input for word in ["how are you", "ela unnav"]):
        return "I am fully operational boss. Ready to assist you!"

    # --- Open Apps ---
    if "open youtube" in user_input:
        import webbrowser
        webbrowser.open("https://youtube.com")
        return "Opening YouTube boss."

    if "open google" in user_input:
        import webbrowser
        webbrowser.open("https://google.com")
        return "Opening Google boss."

    if "open github" in user_input:
        import webbrowser
        webbrowser.open("https://github.com")
        return "Opening GitHub boss."

    if "open naukri" in user_input:
        import webbrowser
        webbrowser.open("https://naukri.com")
        return "Opening Naukri for job search boss."

    # --- Search ---
    if user_input.startswith("search "):
        query = user_input.replace("search ", "")
        import webbrowser
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"Searching for {query} boss."

    # --- System ---
    if any(word in user_input for word in ["shutdown", "stop", "bye", "exit"]):
        return "SHUTDOWN"

    if any(word in user_input for word in ["thank", "thanks", "thanks bro"]):
        return "Always here for you boss!"

    # --- Default ---
    return f"I heard you say: {user_input}. I am still learning boss. More features coming soon!"
