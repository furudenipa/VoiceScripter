# VoiceScripter

# DEMO
簡単な文字起こしソフト  
内部はFaster Whisperで構成
![Alt text](image.png)

# Requirement

* Faster Whisper
* torch
* python 3

# Usage

main.pyで実行  
1. Model Optionから好きなModelを展開  
2. Select Audiofileから文字起こし対象のファイルを選択  
3. 音声データを処理　で文字起こし  
4. 必要があればtxtで保存可能  

# Note
 - faster whisperはPATHを通しておくこと
 - PyTorchのtorch.cuda.is_available()がTrueならGPUを使用、FalseならCPUを使用
 - 日本語の場合はチェックボックスにチェックを入れておくと若干動作が早くなる
 - 初回実行時はModelのダウンロードが挟まるので時間がかかる

↓以下は過去の記述
 - Largeは10GB, Mediumは5GBのVRAMを要求
 - Largeはかなり遅い, 元データの長さとほぼ同時間かかる
 - whisperはPATHを通しておくこと
 - 日本語の場合はチェックボックスにチェックを入れておくと若干動作が早くなる


# License

MIT