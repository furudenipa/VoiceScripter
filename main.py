import tkinter as tk
from voice_model import VoiceModel
from gui import VoiceToTextApp


if __name__ == "__main__":
    root = tk.Tk()
    root.title("VoiceScripter")
    voice_model = VoiceModel()
    app = VoiceToTextApp(root, voice_model)
    root.mainloop()
