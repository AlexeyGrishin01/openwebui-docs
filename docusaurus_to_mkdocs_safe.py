import re
from pathlib import Path
import tkinter as tk
from tkinter import filedialog

# -----------------------------
# Выбор папки docs через диалог
# -----------------------------
root = tk.Tk()
root.withdraw()
docs_dir = filedialog.askdirectory(title="Выбери папку docs")

if not docs_dir:
    print("❌ Папка не выбрана")
    exit()

docs_path = Path(docs_dir)

print(f"📂 Обработка: {docs_path}")


# -----------------------------
# regex правила
# -----------------------------

RE_ANCHOR = re.compile(r'<a id="[^"]*"></a>', re.IGNORECASE)

RE_HTML_WRAPPER = re.compile(
    r'</?(div|section|span|table|tbody|tr|td)[^>]*>',
    re.IGNORECASE
)

RE_MD_IMAGE = re.compile(
    r'!\[([^\]]*)\]\(([^)]+)\)'
)

RE_BAD_HASH_LINK = re.compile(
    r'\(/#([^)]+?)\.md\)'
)

RE_BACKSLASH = re.compile(r'\\')

RE_ADMONITION = re.compile(
    r'^:::\s*(note|tip|warning|info|danger)',
    re.MULTILINE | re.IGNORECASE
)


# -----------------------------
# функции преобразования
# -----------------------------

def md_image_to_html(match):
    alt = match.group(1)
    src = match.group(2)

    # только для локальных assets — внешние не трогаем
    if src.startswith("http"):
        return match.group(0)

    return f'<img src="{src}" alt="{alt}">'


def fix_hash_link(match):
    name = match.group(1)
    name = name.replace("-.", "").replace(".md", "")
    return f"(index.md#{name})"


def fix_admonitions(text):
    def repl(m):
        kind = m.group(1).lower()
        return f"!!! {kind}"
    return RE_ADMONITION.sub(repl, text)


def clean_html_wrappers(text):
    return RE_HTML_WRAPPER.sub("", text)


def process_file(path: Path):
    text = path.read_text(encoding="utf-8")

    original = text

    # удалить docusaurus якоря
    text = RE_ANCHOR.sub("", text)

    # убрать html layout
    text = clean_html_wrappers(text)

    # markdown картинки → html img (чтобы работали внутри HTML)
    text = RE_MD_IMAGE.sub(md_image_to_html, text)

    # hash md ссылки
    text = RE_BAD_HASH_LINK.sub(fix_hash_link, text)

    # admonitions ::: → !!!
    text = fix_admonitions(text)

    # слеши
    text = RE_BACKSLASH.sub("/", text)

    # удалить лишние пустые строки
    text = re.sub(r'\n{3,}', '\n\n', text)

    if text != original:
        path.write_text(text, encoding="utf-8")
        print(f"✔ исправлен: {path.relative_to(docs_path)}")


# -----------------------------
# запуск
# -----------------------------

count = 0

for md in docs_path.rglob("*.md"):
    process_file(md)
    count += 1

print(f"\n✅ Готово. Обработано файлов: {count}")
