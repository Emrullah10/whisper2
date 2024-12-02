import whisper
import requests
import smtplib
from email.message import EmailMessage
from googletrans import Translator


model = whisper.load_model("small")
result = model.transcribe("Motivasyon.mp3")
text = result['text']
print(f"Transcribed text: {text}")


class OpenAI:
    def _init_(self, base_url, api_key=None):
        self.base_url = base_url
        self.api_key = api_key

    def summarize(self, text):
        headers = {
            "Content-Type": "application/json"
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        data = {
            "model": "model-identifier",
            "messages": [
                {"role": "system", "content": "Aşağıdaki metni Türkçe düzyazı olarak ayrıntılı bir şekilde özetleyin ve maddelendirilmiş bir yapılacaklar listesi oluşturun."},
                {"role": "user", "content": text}
            ]
        }

        response = requests.post(f"{self.base_url}/chat/completions", json=data, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {response.status_code}, {response.text}")


client = OpenAI(base_url="http://localhost:1234/v1")
summary_result = client.summarize(text)


summary_text = summary_result['choices'][0]['message']['content']
summary_parts = summary_text.split("To-Do List:")
summary = summary_parts[0].strip()
todo_list_text = summary_parts[1].strip() if len(summary_parts) > 1 else ""
todo_list = [item.strip() for item in todo_list_text.split('\n') if item.strip()]


translator = Translator()


summary_tr = translator.translate(summary, src='en', dest='tr').text
todo_list_tr = [translator.translate(item, src='en', dest='tr').text for item in todo_list]

print("Summary (Türkçe):")
print(summary_tr)
print("\nTo-Do List (Türkçe):")
for i, item in enumerate(todo_list_tr, 1):
    print(f"{i}. {item}")


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


sender_email = "deneme011223@gmail.com"
receiver_email = "filont1010@gmail.com"
password = "hpce pebn wppj lvis"
send_email(summary_tr, todo_list_tr, sender_email, receiver_email, password)