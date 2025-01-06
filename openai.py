import openai
import smtplib
from email.message import EmailMessage
import os
from datetime import datetime

# OpenAI API anahtarınızı buraya ekleyin
openai.api_key = "YOUR_OPENAI_API_KEY"

def transcribe_audio(file_path):
    """
    OpenAI Whisper API ile ses dosyasını metne dönüştürür.
    """
    with open(file_path, "rb") as audio_file:
        response = openai.Audio.transcribe(
            model="whisper-1",  # Whisper modelini seçin
            file=audio_file
        )
    return response["text"]

def summarize_and_todo(text):
    """
    OpenAI GPT modeli ile metni özetler ve yapılacaklar listesi oluşturur.
    """
    prompt = (
        """Aşağıdaki metni işleyerek şu adımları izle:  

        1.Metni Ders Formatında Detaylı Özetle:

        - Konunun Temelini Açıkla: Metindeki her önemli noktayı açık, sistematik ve öğretici bir şekilde özetle.
        - Ders Planına Göre Yapılandır: Konuyu giriş, gelişme ve sonuç bölümlerine ayırarak anlat.
        - Örnekler ve Uygulamalar: Eğer metin bir ders anlatımını içeriyorsa, anlatılan örnekler ve uygulamalar da özete eklenmeli.
        - Anahtar Bilgileri ve İpuçlarını Vurgula: Öğrencinin tekrar çalışmasını kolaylaştıracak şekilde bilgi kutucukları eklenebilir.

        2. **Vurgulayıcı Kelimeleri Tanımla:**  
        - Metindeki önemli kelimeleri ve terimleri belirle.  
        - Her kelime ya da terimin yanına kısa ve net bir tanım ekle.

        3. **Yapılacaklar Listesi:**  
        - Özetlenen metindeki aksiyon gerektiren noktaları tespit et.  
        - Her bir eylemi net ve uygulanabilir bir şekilde maddeler halinde yaz.

        **Çıktı Formatı:**  

        Özet:  
        [Metnin detaylı özeti burada yer alacak.]  

        Vurgulayıcı Kelimeler ve Tanımları:  
        1. [Kelime]: [Tanım]  
        2. [Kelime]: [Tanım]  

        Yapılacaklar Listesi:  
        1. [Birinci yapılacak iş]  
        2. [İkinci yapılacak iş]  

        """
    )
    # OpenAI GPT modelini kullanarak özetleme ve yapılacaklar listesi oluştur
    response = openai.Completion.create(
        model="gpt-4",
        prompt=prompt + text,
        max_tokens=1500,
        temperature=0.7
    )

    content = response.choices[0].text.strip()
    parts = content.split("Yapılacaklar Listesi:")
    summary = parts[0].replace("Özet:", "").strip()
    todo_list = [item.strip() for item in parts[1].split('\n') if item.strip()] if len(parts) > 1 else []
    return summary, todo_list

def send_email(summary, todo_list, sender_email, receiver_email, password, log_file):
    """
    Özet ve yapılacaklar listesini e-posta ile gönderir.
    """
    email_content = f"Özet:\n{summary}\n\nYapılacaklar Listesi:\n" + "\n".join([f"{i+1}. {item}" for i, item in enumerate(todo_list)])
    msg = EmailMessage()
    msg.set_content(email_content)
    msg["Subject"] = "Özet ve Yapılacaklar Listesi (Türkçe)"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, password)
            smtp.send_message(msg)
        email_status = "E-posta başarıyla gönderildi!"
    except Exception as e:
        email_status = f"E-posta gönderiminde hata oluştu: {e}"

    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"Eposta Durumu:\n{email_status}\n")
    print(email_status)

def save_to_file(transcribed_text, summary, todo_list, audio_file_path):
    """
    Transkript, özet ve yapılacaklar listesini bir dosyaya kaydeder.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"output_{timestamp}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Transcribed Text:\n{transcribed_text}\n\n")
        f.write(f"Özet:\n{summary}\n\n")
        f.write("Yapılacaklar Listesi:\n")
        for i, item in enumerate(todo_list, 1):
            f.write(f"{i}. {item}\n")
        
        f.write(f"\nSes Dosyası Metni:\n{audio_file_path}\n")
    print(f"Bilgiler {filename} dosyasına kaydedildi.")
    return filename

if __name__ == "__main__":
    audio_file = "kayit/edebiyat.mp3"
    transcribed_text = transcribe_audio(audio_file)
    print(f"Transcribed text: {transcribed_text}")

    summary, todo_list = summarize_and_todo(transcribed_text)
    print("Özet:")
    print(summary)
    print("\nYapılacaklar Listesi:")
    for i, item in enumerate(todo_list, 1):
        print(f"{i}. {item}")

    log_file = save_to_file(transcribed_text, summary, todo_list, audio_file)

    sender_email = "deneme011223@gmail.com"
    receiver_email = "filont1010@gmail.com"
    password = "hpce pebn wppj lvis"

    send_email(summary, todo_list, sender_email, receiver_email, password, log_file)
