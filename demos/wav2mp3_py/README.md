Use ffmpeg to convert wav audio file to mp3 formate.

使用 Python 的 pydub 套件來將 wav 檔轉換成 mp3。請先安裝必要套件：
以下範例是

```
pip install pydub
```

你還需要安裝 ffmpeg，請到 FFmpeg官網 下載並安裝，或用 Chocolatey：
```
 choco install ffmpeg
```
ubuntu /wsl
可用
```
apt-get install ffmpeg
```

執行方法
```
python wav2mp3.py <輸入wav檔案> <輸出mp3檔案>
```

