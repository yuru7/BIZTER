#!/usr/bin/python3

import os
import shutil
import subprocess
from typing import Any, Tuple
from unicodedata import east_asian_width

import fontforge

VERSION = "v0.0.2"
FONT_NAME = "BIZTER"

BUILD_TMP = "build_tmp"
SOURCE_DIR = "source_fonts"
SOURCE_FONT_JP = "BIZUDPGothic-{}.ttf"
SOURCE_FONT_EN = "Inter-{}.ttf"

EM_ASCENT = 1782
EM_DESCENT = 266

FONT_ASCENT = EM_ASCENT + 60
FONT_DESCENT = EM_DESCENT + 170

COPYRIGHT = """[Inter]
Copyright (c) 2020 The Inter Project Authors (https://github.com/rsms/inter)

[BIZ UDPGothic]
Copyright 2022 The BIZ UDGothic Project Authors (https://github.com/googlefonts/morisawa-biz-ud-gothic)

[BIZTER]
Copyright 2022 Yuko Otawara
"""


def open_font(weight) -> Tuple[Any, Any]:
    """フォントファイルを開く"""
    jp_font = fontforge.open(f"{SOURCE_DIR}/{SOURCE_FONT_JP.format(weight)}")
    if weight == "Bold":
        # 太さを合わせるため、InterはSemiBoldを使う
        en_font = fontforge.open(f"{SOURCE_DIR}/{SOURCE_FONT_EN.format('Semi'+weight)}")
    else:
        en_font = fontforge.open(f"{SOURCE_DIR}/{SOURCE_FONT_EN.format(weight)}")
    return jp_font, en_font


def remove_duplicate_glyphs(jp_font, en_font):
    """Interと重複しているグリフを削除する"""
    for g in en_font.glyphs():
        if not g.isWorthOutputting():
            continue
        unicode = int(g.unicode)
        if unicode >= 0:
            for g_jp in jp_font.selection.select(unicode).byGlyphs:
                # East Asian Ambiguous Widthの文字は、Inter側のグリフを削除する
                if east_asian_width(chr(unicode)) == "A":
                    g.clear()
                else:
                    g_jp.clear()


def merge_fonts(jp_font, en_font, weight) -> Any:
    """英語フォントと日本語フォントをマージする"""
    # マージするためにemを揃える
    em_size = EM_ASCENT + EM_DESCENT
    jp_font.em = em_size
    en_font.em = em_size

    en_font.generate(f"{BUILD_TMP}/modified_{SOURCE_FONT_EN.format(weight)}")
    jp_font.mergeFonts(f"{BUILD_TMP}/modified_{SOURCE_FONT_EN.format(weight)}")
    return jp_font


def edit_meta_data(font, weight: str):
    """フォント内のメタデータを編集する"""
    font.ascent = EM_ASCENT
    font.descent = EM_DESCENT
    font.os2_typoascent = EM_ASCENT
    font.os2_typodescent = -EM_DESCENT

    font.hhea_ascent = FONT_ASCENT
    font.hhea_descent = -FONT_DESCENT
    font.os2_winascent = FONT_ASCENT
    font.os2_windescent = FONT_DESCENT
    font.hhea_linegap = 0
    font.os2_typolinegap = 0

    font.sfnt_names = (
        (
            "English (US)",
            "License",
            "This Font Software is licensed under the SIL Open Font License, Version 1.1. This license is available with a FAQ at: http://scripts.sil.org/OFL",
        ),
        ("English (US)", "License URL", "http://scripts.sil.org/OFL"),
        ("English (US)", "Version", f"{FONT_NAME} {VERSION}"),
    )
    font.familyname = FONT_NAME
    font.fontname = f"{FONT_NAME}-{weight}"
    font.fullname = f"{FONT_NAME} {weight}"
    font.os2_vendor = "TWR"
    font.copyright = COPYRIGHT


def main():
    # 一時ディレクトリ作成
    if os.path.exists(BUILD_TMP):
        shutil.rmtree(BUILD_TMP)
    os.makedirs(BUILD_TMP)

    for weight in ("Regular", "Bold"):
        jp_font, en_font = open_font(weight)

        remove_duplicate_glyphs(jp_font, en_font)

        font = merge_fonts(jp_font, en_font, weight)

        edit_meta_data(font, weight)

        font.generate(f"{BUILD_TMP}/gen_{FONT_NAME}-{weight}.ttf")

        subprocess.run(
            (
                "python3",
                "-m",
                "ttfautohint",
                "--dehint",
                f"{BUILD_TMP}/gen_{FONT_NAME}-{weight}.ttf",
                f"{BUILD_TMP}/{FONT_NAME}-{weight}.ttf",
            )
        )


if __name__ == "__main__":
    main()
