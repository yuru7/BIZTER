import fontforge

new_font = fontforge.open("source_fonts/BIZUDPGothic-Regular.ttf")
with open("build_tmp/attr_bizud.txt", mode="w", encoding="utf_8") as f:
    for item in dir(new_font):
        f.write(f"{item}: " + str(getattr(new_font, item)) + "\n")
