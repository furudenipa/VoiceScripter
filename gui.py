import tkinter as tk
from tkinter import filedialog, StringVar, BooleanVar, messagebox
import threading
import time
import os.path

MAX_LENGTH=20

class VoiceToTextApp:
    def __init__(self, root, voice_model):
        self.root = root
        self.voice_model = voice_model
        self.audio_path = None
        
        #------モデル関連をpackするframe------
        self.model_frame=tk.LabelFrame(self.root, text="Model Option", bd=5)
        self.model_frame.pack()

        ## モデルサイズを選択するプルダウンリスト
        self.model_size_var = StringVar(self.root)
        self.model_size_var.set("tiny")
        self.model_size_menu = tk.OptionMenu(self.model_frame, self.model_size_var, "tiny", "base", "small", "medium", "large")
        self.model_size_menu.config(width=6)
        self.model_size_menu.pack(side="left")

        ## モデルを展開するボタン
        self.load_button = tk.Button(self.model_frame, width=20, text="モデルを展開", command=self.load_model)
        self.load_button.pack(side="left")

        ## 展開したモデル名
        self.loaded_model_label = tk.Label(self.model_frame, width=20, anchor="w", text="Model: none")
        self.loaded_model_label.pack(side="left")

        #------音声ファイル関連をpackするframe------
        self.audio_path_frame = tk.LabelFrame(self.root, text="Select Audiofile", bd=5)
        self.audio_path_frame.pack()

        ## 音声ファイルを選択するボタン
        self.select_file_button = tk.Button(self.audio_path_frame, width=20, text="音声ファイルを選択", command=self.select_file)
        self.select_file_button.pack(side="left")

        ## 選択した音声ファイル名
        self.selected_file_label = tk.Label(self.audio_path_frame, width=30, anchor="w", text = "Filename: none")
        self.selected_file_label.pack(side="left")

        #------オプションボックス------
        self.options_frame = tk.Frame(self.root, bd=5)
        self.options_frame.pack()

        ## ラジオボタン 改行ありorなし
        self.newline_option = BooleanVar(value=True)  # True = 改行あり, False = 改行なし
        newline_checkbox = tk.Checkbutton(self.options_frame, text="改行を含む", variable=self.newline_option)
        newline_checkbox.pack(side="left")

        ## ラジオボタン lang = ja or Other
        self.lang_option = BooleanVar(value=True)  # True = ja, False = None
        lang_checkbox = tk.Checkbutton(self.options_frame, text="日本語", variable=self.lang_option)
        lang_checkbox.pack(side="left")

        # 音声データを処理するボタン
        self.transcribe_button = tk.Button(self.root, width=20, text="音声データを処理", command=self.transcribe)
        self.transcribe_button.pack()

        # 保存
        self.save_button = tk.Button(self.root, text="結果を保存", command=self.save_result)
        self.save_button.pack()

        # 結果表示エリア
        self.result_text = tk.Text(self.root, wrap=tk.WORD, height=10) # wrap=tk.WORD で折り返しを行う
        self.result_text.pack(expand=True, fill=tk.BOTH)
        
        # 縦方向のスクロールバー
        self.scrollbar = tk.Scrollbar(self.result_text, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def load_model(self):
        def _load():
            self.load_button.config(state=tk.DISABLED, text="モデルを展開中...")
            self.transcribe_button.config(state=tk.DISABLED,text="音声データを処理")

            model_size = self.model_size_var.get()
            self.voice_model.load_model(model_size)
            self.loaded_model_label.config(text=f"Model: {model_size}")

            self.load_button.config(state=tk.NORMAL, text="モデルを展開")
            self.transcribe_button.config(state=tk.NORMAL, text="音声データを処理")

        threading.Thread(target=_load).start()

    def select_file(self):
        self.audio_path = filedialog.askopenfilename(
            title="Select an audio file",
            filetypes=[
                ("Audio Files", "*.mp3 *.wav *.m4a"),
                ("MP3 Files", "*.mp3"),
                ("WAV Files", "*.wav"),
                ("M4A Files", "*.m4a"),
                ("All Files", "*.*")
            ]
        )

        # label 更新
        file_name = os.path.basename(self.audio_path)
        display_text = (file_name[:MAX_LENGTH] + '...') if len(file_name) > MAX_LENGTH else file_name
        self.selected_file_label.config(text=f"Filename: {display_text}")

    def transcribe(self):
        if self.audio_path:
            def _transcribe():
                # button を止める
                self.transcribe_button.config(state=tk.DISABLED, text="音声データを処理中...")
                self.load_button.config(state=tk.DISABLED, text="モデルを展開")

                result = self.voice_model.transcribe(self.audio_path, self.lang_option.get(), self.newline_option.get())
                
                # 結果をTextウィジェットに追加
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, result)
                
                # buttonを使用可能に
                self.transcribe_button.config(state=tk.NORMAL, text="音声データを処理")
                self.load_button.config(state=tk.NORMAL, text="モデルを展開")

            threading.Thread(target=_transcribe).start()
        else:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Please select audiofile!!")

    def save_result(self):
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
            initialfile=f"transcript_{int(time.time())}.txt"
        )
        
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.result_text.get(1.0, tk.END))
            messagebox.showinfo("保存完了", "結果をファイルに保存しました。")
