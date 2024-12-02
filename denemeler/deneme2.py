import whisper

# Whisper modeli yükleniyor
model = whisper.load_model("small")

# Ses dosyasını metne çevirme
result = model.transcribe("kayit.wav")

# Çıktıyı yazdırma
print("Transkript:", result["text"])
