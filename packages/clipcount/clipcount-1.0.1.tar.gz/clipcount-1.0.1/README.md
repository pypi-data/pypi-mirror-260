# clipcount
![GitHub License](https://img.shields.io/github/license/yusu79/clipcount)
![PyPI - Version](https://img.shields.io/pypi/v/clipcount)
![PyPI - Downloads](https://img.shields.io/pypi/dm/clipcount)

クリップボードの文字を読み込み、文字数を出力するPythonパッケージです。

[Read this in English.](https://github.com/yusu79/clipcount/blob/main/README_en.md)


<!-- omit in toc -->
- [インストール（Setup）](#インストールsetup)
- [使い方（Quick usage）](#使い方quick-usage)
- [解説（Usage）](#解説usage)
- [使用しているパッケージ (Dependencies)](#使用しているパッケージ-dependencies)

## インストール（Setup）
pipでインストールします。
```bash:
pip install clipcount
```
### Windowsで「警告」が出た時の対処方法

Windowsで上記のコマンドを実行した際に「`"WARNING: The script clipcount.exe is installed in 'ファイルパス' which is not on PATH."`」が表示されたなら、以下の記事をご参照ください。

参考: [【Python Windows】pip install でPATHが通らない時の解決方法 | ゆすノート](https://yusu79.com/python-path-issue/)

「`WARNING: Failed to write executable - trying to use .deleteme logic`」が表示されたなら、管理者権限でターミナルを実行した上でインストールしてください。詳しくは以下の記事をご参照ください。

参考: [Error installing package with executable · Issue #9023 · pypa/pip](https://github.com/pypa/pip/issues/9023)


## 使い方（Quick usage）
| オプション          | 説明                                                                     | 
| ------------------- | ------------------------------------------------------------------------ | 
| clipcount -h        | ヘルプ画面を表示します。                                                 | 
| clipcount --help_jp | ヘルプ画面を日本語で表示します。                                         | 
| clipcount -b        | 改行コード（`\n`か`\r\n`）を削除した文字数を出力します。                 | 
| clipcount -s        | 半角空白を削除した文字数を出力します。                                   | 
| clipcount -S        | 全角空白を削除した文字数を出力します。                                   | 
| clipcount -t        | タブコード（`\t`）を削除した文字数を出力します。                                       | 
| clipcount --split   | 空白文字（改行、半角空白、全角空白、タブ）を削除した文字数を出力します。 | 
| clipcount -m        | 半角英数を0.5文字として換算して、文字数を出力します。                    | 


CUIツールとして使用し、文字数をターミナル上に出力できます。
```bash:
clipcount [オプション]
```

また、Pythonファイル上でインポートできます。
```python:
from clipcount import clipcount
x = clipcount({オプション})
```



### 使用例（Example）
*※以下の例は「Windows」環境で実行しているので、改行コードを「`\r\n`」としてカウントしています。*

以下の文章をコピーした上で、clipcountを実行します。
```md:
clipboardの
文字　を読み込みます。
```

#### CUI
- そのまま実行する
```bash:
# 空白文字を含めた全ての文字数を出力
$ clipcount
23
```
- 半角空白を削除して出力
```bash:
# 上記の空白は全角空白なので何も変わらない
$ clipcount -s
23
```
- 全角空白を削除する
```bash:
# 全角空白が1文字削除されて出力
$ clipcount -S
22
```
- 半角空白を削除して出力
```bash:
# 改行コードが削除されて出力
$ clipcount -b
21
```
- 空白文字全てを削除して出力
```bash:
# 全角空白文字が削除される
$ clipcount -sSbt
20
```
もしくは`--split`を使っても同じ結果がでる。
```bash:
# 全角空白文字が削除される
$ clipcount --split
20
```

- 半角英数を0.5文字として換算して出力
```bash:
# 半角英数は0.5文字になる
$ clipcount -m
17.5
```

#### インポート
Pythonファイルで「import」も出来ます。
注意点として、オプションに渡すコマンドは「`-`」や「`--`」は除いたものしてください。
```python:
# クリップボードの文字数を変数に格納できる
from clipcount import clipcount
x = clipcount({"split"})
print(x)
```
```bash:
# 「clipcount --split」と同じ結果となる
$ python hoge.py
20
```


## 解説（Usage）
clipcountは、「クリップボードを読み込み、文字数を出力する」Pythonパッケージです。
デフォルトでは、「**空白文字（改行、半角空白、全角空白、タブ）を含めた文字数**」を出力します。また、半角文字と全角文字のどちらも「**同じ1文字**」として換算しています。

各種オプションで、それぞれの空白文字を削除した文字数を出力できます。
ターミナル上で使用する場合、オプションは組み合わせる事ができるので、例えば、「全角空白とタブのみ削除した文字数を出力する」には「`clipcount -St`」とすると良いです。

もし、空白文字を一括で削除したい場合は「`--split`」オプションが使えます。これは「`-bsSt`」と同じ意味となります。

半角文字と全角文字を分けて換算したい場合は「`-m`」オプションが使えます。これは半角文字を「**0.5文字として換算する**」オプションです。WordPressのタイトルやメタキーワードなどの文字数を気にする場面で使用すると、良いと思われます。



## 使用しているパッケージ (Dependencies)
- [pyperclip](https://github.com/asweigart/pyperclip)
