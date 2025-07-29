from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
import requests

load_dotenv()
app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/message", methods=["POST"])
def message():
    user_msg = request.json.get("message")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GEMINI_API_KEY}"
    }
    data = {
        "contents": [{
            "parts": [{"text": user_msg}]
        }]
    }
    res = requests.post("https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + GEMINI_API_KEY,
                        headers=headers, json=data)
    try:
        reply = res.json()["candidates"][0]["content"]["parts"][0]["text"]
    except:
        reply = "Sorry, I couldn't generate a reply."
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
