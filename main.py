from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import anthropic
import os

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def analiz_et(mesaj):
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": f"""Aşağıdaki WhatsApp mesajını analiz et ve JSON formatında yanıt ver.
            
Mesaj: "{mesaj}"

Şu formatta yanıt ver:
{{
  "tip": "not" veya "randevu" veya "belirsiz",
  "ozet": "kısa özet",
  "tarih": "varsa tarih (örn: Yarın, 15 Mart, vb) yoksa null",
  "saat": "varsa saat (örn: 15:00) yoksa null"
}}

Sadece JSON döndür, başka hiçbir şey yazma."""
        }]
    )
    return response.content[0].text

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "")
    
    print(f"Mesaj geldi: {incoming_msg} | Kimden: {sender}")
    
    try:
        analiz = analiz_et(incoming_msg)
        print(f"AI Analizi: {analiz}")
        
        import json
        sonuc = json.loads(analiz)
        
        if sonuc["tip"] == "randevu":
            cevap = f"📅 Randevu kaydedildi!\n📝 {sonuc['ozet']}"
            if sonuc["tarih"]:
                cevap += f"\n📆 Tarih: {sonuc['tarih']}"
            if sonuc["saat"]:
                cevap += f"\n⏰ Saat: {sonuc['saat']}"
        elif sonuc["tip"] == "not":
            cevap = f"📝 Not kaydedildi!\n{sonuc['ozet']}"
        else:
            cevap = f"🤔 Anladım: {sonuc['ozet']}"
            
    except Exception as e:
        print(f"Hata: {e}")
        cevap = "⚠️ Mesaj analiz edilirken hata oluştu."
    
    response = MessagingResponse()
    msg = response.message()
    msg.body(cevap)
    
    return str(response)

@app.route("/")
def home():
    return "WhatsApp Not Toplayici calisıyor! 🚀"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
