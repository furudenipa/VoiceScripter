import whisper
import time
from datetime import timedelta
x = 0
class DummyVoiceModel:
    def __init__(self):
        self.is_loaded = False
        self.model = None

    def load_model(self, size):
        self.model=whisper.load_model(size)
        self.is_loaded = True

    def transcribe(self, audio_path, lang_option, newline_option):
        if not self.is_loaded:
            return "モデルがロードされていません。"
        
        if lang_option:
            lang = "ja"
        else:
            lang = None

        result=self.model.transcribe(audio_path, language=lang)
        if newline_option:
            formatted_segments = []
            for segment in result["segments"]:
                start = format_time(segment["start"])
                end = format_time(segment["end"])
                text = segment["text"]
                formatted_segments.append(f"[{start} --> {end}] {text}")
            return '\n'.join(formatted_segments)
  
        else:
            return result["text"]

def format_time(seconds):
        return str(timedelta(seconds=seconds))

    