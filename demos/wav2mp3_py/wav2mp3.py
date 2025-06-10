from pydub import AudioSegment
import os
import sys

def wav_to_mp3(wav_path, mp3_path):
    audio = AudioSegment.from_wav(wav_path)
    audio.export(mp3_path, format="mp3")
    print(f"已將 {wav_path} 轉換為 {mp3_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python wav2mp3.py <輸入wav檔案> <輸出mp3檔案>")
        sys.exit(1)
    wav_file = sys.argv[1]
    mp3_file = sys.argv[2]
    wav_to_mp3(wav_file, mp3_file)