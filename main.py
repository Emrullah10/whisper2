# import whisper

# model = whisper.load_model("base")

# result = model.transcribe("C:\\Users\\Aslı Gül KALKAN\\PycharmProjects\\whisper_project\\kayit.wav")

# print(result["text"])


import whisper
import torch

#model = whisper.load_model("large")
device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("medium", device=device)

audio_file = "C:\\Users\\kemal\\Desktop\\whisper\\ders.mp3"


result = model.transcribe(audio_file, language="tr")


print(result["text"])