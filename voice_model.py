from faster_whisper import WhisperModel
import torch
x = 0
class VoiceModel:
    def __init__(self):
        self.is_loaded = False
        self.model = None
        if torch.cuda.is_available():
            self.device = "cuda"
        else:
            self.device = "cpu"

    def load_model(self, size):
        self.model= WhisperModel(
            model_size_or_path = size ,
            device = self.device,
            compute_type = "int8_float16" if self.device == "cuda" else "int8",
        )
        self.is_loaded = True

    def transcribe(self, audio_path, lang_option, timestamp_option):
        if not self.is_loaded:
            return "モデルがロードされていません。"
        
        if lang_option:
            lang = "ja"
        else:
            lang = None
        
        segments, _ = self.model.transcribe(audio_path, word_timestamps=True, language=lang)
       
        transcripts = [f"[info] This document is transcribed using: {self.device}"]
        timelines = [f"[info] This document is transcribed using: {self.device}"]
        for segment in segments:
            timeline = f"[{int(segment.start // 60)}m{int(segment.start % 60)}s -> {int(segment.end // 60)}m{int(segment.end % 60)}s] {segment.text.strip()}"

            timelines.append(timeline)
            transcripts.append(segment.text)

        if timestamp_option:
            return "\n".join(timelines)
        else:
            return "\n".join(transcripts)

    