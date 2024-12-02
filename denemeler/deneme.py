import google.generativeai as genai

api_key = "AIzaSyBOdu46fWM8OyNQdk3oST-vzzck1cj9I7c"
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("türkiye hakkında bilgi ver")
print(response.text)
