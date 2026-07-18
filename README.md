# whisper2

Speech-to-text transcription and AI-powered summarization pipeline built with Python. Audio recordings (lectures, meetings) are transcribed with **OpenAI Whisper** and then summarized with an LLM, producing structured text output. Related to my TUBITAK 2209-supported graduation project on making academic content accessible.

## How it works

`transkript.py` and `onlyWhisper.py` handle transcription with Whisper. `openai.py` sends transcripts to the OpenAI API for summarization with custom prompts. `main.py` ties the pipeline together and writes results to the output folders.

## Getting started

```bash
pip install -r requirements.txt
python main.py
```

Set your OpenAI API key as an environment variable before running.
