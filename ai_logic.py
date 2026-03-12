import os
from dotenv import load_dotenv
from gigachat import GigaChat

import speech_recognition as sr
from pydub import AudioSegment

load_dotenv()
credentials = os.getenv("CREDENTIALS")

def transcribe_voice(file_path):
    print("Начинаю конвертацию аудио...")
    wav_path = "voice.wav"

    audio = AudioSegment.from_ogg(file_path)
    audio.export(wav_path, format="wav")

    print("Начинаю распознование текста...")
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="ru_RU")
            return text
        except sr.UnknownValueError:
            return "Извини, я не смог распознать слова в этом голосовом сообщении."
        except sr.RequestError:
            return "Ошибка связи с сервером распознования голоса."

def get_summary(text):
    with GigaChat(credentials=credentials, verify_ssl_certs=False) as giga:
        response = giga.chat(
            {
            "messages":
            [
                {
                "role": "system",
                "content": "Ты умный AI-ассистент. Твоя задача - Прочитать текст и сделать из него выжимку, описать кто говорит, о чём и суть сообщения"
                },
                {
              "role": "user",
                "content": text
                }
            ]
        }
        )
        return response.choices[0].message.content
