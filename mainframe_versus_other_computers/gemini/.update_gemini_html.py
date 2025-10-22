""" 
    Program to update Gemini HTML responses
"""

import os
import glob

files = glob.glob("gemini_html\\*.html")
for filename in files:
    with open(filename, 'r', encoding="utf-8") as file:
        content = file.read()
        file.close()
    if "<!DOCTYPE" != content[:9]:
        continue
    print("processing file", filename)
    content = content.split("<body", 1)[1].split(">",1)[1].split("</body",1)[0]
    desc = os.path.basename(filename).split(".")
    desc.pop(-1)
    desc = ".".join(desc)
    content = '<p align="center"><font style="font-size: 14pt; font-weight: bold;">I asked Gemini "' + desc + '"</font></p>\n' + content
    with open(filename, 'w', encoding="utf-8") as file:
        file.write(content)
        file.close()


