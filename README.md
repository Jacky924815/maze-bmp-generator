# maze-bmp-generator
![](maze-2a.png)

## Usage
執行以下命令就會產生 62 張隨機迷宮的 BMP 與文字檔；生成的檔案會放在 `output/image` 與 `output/data` 裡。
```
python maze_gen.py
```

## Dependency
需要安裝以下 Python 套件：
- numpy
- opencv-python
- PIL


## Caution
生成檔案前請先確認路徑 `output/image` 與 `output/data` 是否存在。
