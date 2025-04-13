# BIZTER

BIZTER は、UI 向けフォント [Inter](https://github.com/rsms/inter) と、ユニバーサルデザインフォントの [BIZ UDPゴシック](https://github.com/googlefonts/morisawa-biz-ud-gothic) の合成フォントです。

Inter はとても美しい… BIZ UDPゴシックはとても読みやすい… ならば、それらを組み合わせたフォントが読みやすく美しいフォントにならないはずがない！  
…というモチベーションで組み合わせたところ、やっぱり最高でした。

👉 [ダウンロード](https://github.com/yuru7/BIZTER/releases)  
※「Assets」内の zip ファイルをダウンロードしてご利用ください。

![image](https://user-images.githubusercontent.com/13458509/208080375-44309b06-b563-4f08-86d0-c7f74e677beb.png)

## ビルド

### ビルド環境

- OS: `Ubuntu 22.04.1 LTS`
- Python: `3.10.6`
- FontForge: `20201107`
- ttfautohint: `1.8.3`

### Linux

```sh
# 必要パッケージのインストール
sudo apt install python3 python3-pip fontforge python3-fontforge ttfautohint
# ビルド
python build.py
```

### Windows

**※事前にPython3、FontForgeをインストールしてあること**

```sh
&"C:\Program Files (x86)\FontForgeBuilds\bin\ffpython.exe" .\build.py
```
