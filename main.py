from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "")
    
    print(f"Mesaj geldi: {incoming_msg} | Kimden: {sender}")
    
    response = MessagingResponse()
    msg = response.message()
    msg.body(f"✅ Mesajın alındı: '{incoming_msg}'")
    
    return str(response)

@app.route("/")
def home():
    return "WhatsApp Not Toplayici calisıyor! 🚀"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
