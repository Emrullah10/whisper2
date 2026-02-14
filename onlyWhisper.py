import whisper
from datetime import datetime
import os

def transcribe_audio(file_path):
    """Verilen ses dosyasını Whisper ile metne çevirir."""
    model = whisper.load_model("large")  # İstersen 'base', 'medium', 'large' yapabilirsin
    print("Ses dosyası işleniyor...")
    result = model.transcribe(file_path)
    return result['text']

def save_transcription(text, output_dir="transcriptions"):
    """Metni zaman damgalı bir .txt dosyasına kaydeder."""
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(output_dir, f"transcription_{timestamp}.txt")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"✅ Metin başarıyla kaydedildi: {filename}")
    return filename

if __name__ == "__main__":
    # Ses dosyasının yolu
    audio_file = r"kayit/enerjisa-regülasyon.mp3"  # örnek: "kayit/ders.mp3"

    # Transkripsiyon işlemi
    text = transcribe_audio(audio_file)

    # .txt dosyasına kaydetme
    save_transcription(text)
