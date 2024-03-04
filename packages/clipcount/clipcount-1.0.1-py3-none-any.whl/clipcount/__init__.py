import sys
import pyperclip
import unicodedata

def usage():
    print("""
Usage: clipcount [options]

Description: Reads the clipboard and outputs the character count.

Features: By default, it outputs the character count, including whitespace characters (line breaks, spaces, full-width spaces, tabs).

Arguments: None

Options:
    -h|--help           Display help
       --help_jp        Display help in Japanese
    -b|--no-break       Exclude line breaks
    -s|--no-space       Exclude half-width spaces
    -S|--no-SPACE       Exclude full-width spaces
    -t|--no-tab         Exclude tabs
       --split          Exclude whitespace characters (line breaks, half-width spaces, full-width spaces, tabs)
    -m|--multi          Treat half-width alphanumeric characters as 0.5 characters each


""")
def usage_jp():
    print("""
使用法: clipcount [オプション] 

説明: クリップボードを読み取り、文字数を出力します。

特徴: デフォルトでは、空白文字（改行、半角空白、全角空白、タブ）を含めた文字数を出力します。

引数: 無し

オプション:
    -h|--help           ヘルプを表示します
       --help_jp        日本語のヘルプを表示します
    -b|--no-break       改行削除
    -s|--no-space       半角空白削除
    -S|--no-SPACE       全角空白削除
    -t|--no-tab         タブ削除
       --split          空白文字（改行、半角空白、全角空白、タブ）削除
    -m|--multi          半角英数を0.5文字として換算する

""")


def len_text(text):
    count = 0
    for c in text:
        if unicodedata.east_asian_width(c) in 'FWA':
            count += 1
        else:
            count += 0.5
    return count

def clipcount(options=set()):
    if options=={}: options=set()
    txt = "".join(pyperclip.paste())

    if {"split"} <= options:
        txt = "".join(txt.split())
    else:
        if {"b"} <= options or {"no-break"} <= options:
            txt = "".join(txt.splitlines())
        if {"s"} <= options or {"no-space"} <= options:
            txt = "".join(txt.split(" "))
        if {"S"} <= options or {"no-SPACE"} <= options:
            txt = "".join(txt.split("　"))
        if {"t"} <= options or {"no-tab"} <= options:
            txt = "".join(txt.split("\t"))

    if {"m"} <= options or {"multi"} <= options:
        return len_text(txt)
    else: 
        return len(txt) 

def main():
    i = 1
    options = set()  # 使用されたオプションを保存するための集合
    try:
        while i < len(sys.argv):
            if sys.argv[i] in ["-h", "--help"]:
                usage()
                sys.exit(0)
            elif sys.argv[i] in ["--help_jp"]:
                usage_jp()
                sys.exit(0)
            elif sys.argv[i] in ["--split"]:
                options.update({sys.argv[i][2:]})
                i += 1
            elif sys.argv[i] in ["--no-break"]:
                options.update({sys.argv[i][2:]})
                i += 1
            elif sys.argv[i] in ["--no-space"]:
                options.update({sys.argv[i][2:]})
                i += 1
            elif sys.argv[i] in ["--no-SPACE"]:
                options.update({sys.argv[i][2:]})
                i += 1
            elif sys.argv[i] in ["--no-tab"]:
                options.update({sys.argv[i][2:]})
                i += 1
            elif sys.argv[i] in ["--multi"]:
                options.update({sys.argv[i][2:]})
                i += 1
            elif sys.argv[i].startswith("--"):
                print("\033[91mError: Invalid Option\n無効なオプションです。--help を使用してください。\033[0m")
                sys.exit(1)
            elif sys.argv[i].startswith("-"):
                # オプションが複数組み合わさっている場合も考慮して、一文字ずつ分割
                options.update(sys.argv[i][1:])
                i += 1
            else:
                i += 1
    except Exception as e:
        print(e)
        print(f"\033[91mエラーです\033[0m")

    print(clipcount(options))


