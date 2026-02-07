import re
from pathlib import Path
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

docs_path = Path(filedialog.askdirectory(title="Выбери папку docs"))
print("Docs:", docs_path)

anchor_re = re.compile(r'<a id="[^"]+"></a>')
backslash_re = re.compile(r'assets\\')

def fix_links(text):
    text = text.replace("https://docs.openwebui.com/", "")
    text = text.replace("/#", "#")
    text = text.replace(".md)", ".md)")
    return text

def fix_admonitions(text):
    text = re.sub(r'\ninfo\n', '\n!!! info\n', text)
    text = re.sub(r'\nwarning\n', '\n!!! warning\n', text)
    text = re.sub(r'\nnote\n', '\n!!! note\n', text)
    text = re.sub(r'\ntip\n', '\n!!! tip\n', text)
    return text

for md in docs_path.rglob("*.md"):
    txt = md.read_text(encoding="utf-8")

    txt = anchor_re.sub("", txt)
    txt = txt.replace("\\", "/")
    txt = fix_links(txt)
    txt = fix_admonitions(txt)

    md.write_text(txt, encoding="utf-8")
    print("OK:", md)

print("Done.")
