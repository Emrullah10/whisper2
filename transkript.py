import google.generativeai as genai
import os

genai.configure(api_key=os.environ["AIzaSyBOdu46fWM8OyNQdk3oST-vzzck1cj9I7c"])
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Write a story about a magic backpack.")
print(response.text)