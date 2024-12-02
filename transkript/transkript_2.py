import whisper
import google.generativeai as genai
import smtplib
from email.message import EmailMessage


API_KEY = "AIzaSyBOdu46fWM8OyNQdk3oST-vzzck1cj9I7c"
genai.configure(api_key=API_KEY)


def transcribe_audio(file_path):
    model = whisper.load_model("small")
    result = model.transcribe(file_path)
    return result['text']


def summarize_and_todo(text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = (
        "Metni özetleyin ve bir yapılacaklar listesi oluşturun. Çıktı formatı şu şekilde olmalı:\n"
        "Özet:\n[Özet metni]\n\nYapılacaklar Listesi:\n1. [İlk madde]\n2. [İkinci madde]\n"
    )
    response = model.generate_content(prompt + text)
    content = response.text

    
    parts = content.split("Yapılacaklar Listesi:")
    summary = parts[0].replace("Özet:", "").strip()
    todo_list = [item.strip() for item in parts[1].split('\n') if item.strip()] if len(parts) > 1 else []
    return summary, todo_list


def send_email(summary, todo_list, sender_email, receiver_email, password):
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
        print("E-posta başarıyla gönderildi!")
    except Exception as e:
        print(f"E-posta gönderiminde hata oluştu: {e}")


if __name__ == "__main__":
    
    audio_file = "ders.mp3"
    transcribed_text = transcribe_audio(audio_file)
    print(f"Transcribed text: {transcribed_text}")

    
    summary, todo_list = summarize_and_todo(transcribed_text)
    print("Özet:")
    print(summary)
    print("\nYapılacaklar Listesi:")
    for i, item in enumerate(todo_list, 1):
        print(f"{i}. {item}")

    
    sender_email = "deneme011223@gmail.com"
    receiver_email = "filont1010@gmail.com"
    password = "hpce pebn wppj lvis"

    
    send_email(summary, todo_list, sender_email, receiver_email, password)
