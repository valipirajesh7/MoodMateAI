
from http.server import BaseHTTPRequestHandler
import json
import random

RESPONSES = {
    "Happy": [
        "That's wonderful! 😊 Keep spreading your happiness. Celebrate the little things! ✨",
        "Your happiness is precious! 🌻 Keep smiling and sharing your positive energy."
    ],
    "Sad": [
        "It's okay to feel sad sometimes. 💙 Be gentle with yourself. Brighter days can come. 🌈",
        "Sending you a little warmth. 🤗 You don't have to be strong every moment."
    ],
    "Stressed": [
        "Take a slow breath. 🌿 You don't have to solve everything at once. Choose one small step. 💪",
        "Pause for a moment. 🫶 Focus on what you can control, one thing at a time."
    ],
    "Angry": [
        "It's okay to feel angry. 💙 Pause before reacting and give yourself time to think. 🌱"
    ],
    "Loved": [
        "What a beautiful feeling! 🥰 You deserve kindness, love, and connection. 💖"
    ],
    "Tired": [
        "Rest is productive too! 🌙 Take a break, recharge, and return when you're ready. 💙"
    ],
    "Worried": [
        "You don't need all the answers today. 💙 Take one small step toward what matters. 🌱"
    ],
    "Motivated": [
        "That's the spirit! 🚀 Take one small action today. Consistency matters more than perfection. 🔥"
    ]
}


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/api":
            self.send_error(404)
            return

        try:
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length))

            mood = data.get("mood", "Happy")
            feelings = str(data.get("feelings", "")).strip()
            name = str(data.get("name", "friend")).strip() or "friend"

            if mood not in RESPONSES:
                mood = "Happy"

            reply = random.choice(RESPONSES[mood])

            if feelings:
                reply = (
                    f"Hey {name} 💙, thank you for sharing. "
                    f"I hear you: {feelings[:250]}. "
                    f"Here's a little encouragement: {reply}"
                )
            else:
                reply = f"Hey {name} 💙, {reply}"

            body = json.dumps({"reply": reply}).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)

        except (ValueError, TypeError, json.JSONDecodeError):
            self.send_error(400, "Invalid JSON request")

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
