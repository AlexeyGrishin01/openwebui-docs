import re
import json
import os
from pathlib import Path
import yaml

ROOT = Path(".")
DOCS = ROOT / "docs"
MKDOCS = ROOT / "mkdocs.yml"

# -------------------------
# SAFE FILE IO
# -------------------------

def read_text_safe(p: Path):
    return p.read_text(encoding="utf-8", errors="ignore")

def write_text_safe(p: Path, text: str):
    p.write_text(text, encoding="utf-8", newline="\n")

# -------------------------
# FRONTMATTER CLEAN
# -------------------------

def strip_frontmatter(text):
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return parts[2].lstrip()
    return text

# -------------------------
# MDX → MD CLEAN
# -------------------------

def clean_mdx(text):
    text = re.sub(r"^import .*?$", "", text, flags=re.M)
    text = re.sub(r"^export .*?$", "", text, flags=re.M)
    text = re.sub(r"<[A-Z][^>]*>", "", text)
    text = re.sub(r"</[A-Z][^>]*>", "", text)
    text = re.sub(r"{[^{}]*}", "", text)
    return text

# -------------------------
# ADMONITIONS
# -------------------------

def convert_admonitions(text):
    text = re.sub(
        r"::: *(info|warning|tip|note|danger|caution)\s*(.*)",
        lambda m: f'!!! {m.group(1)} "{m.group(2).strip()}"',
        text
    )
    text = re.sub(r"^:::\s*$", "", text, flags=re.M)
    text = re.sub(
        r"^info +(.*)",
        lambda m: f'!!! info "{m.group(1)}"',
        text,
        flags=re.M
    )
    return text

# -------------------------
# TABS → MATERIAL
# -------------------------

def convert_tabs(text):
    text = re.sub(r"<Tabs.*?>", "=== ", text)
    text = re.sub(r"</Tabs>", "", text)
    text = re.sub(
        r"<TabItem value=\"(.*?)\".*?>",
        lambda m: f'=== "{m.group(1)}"',
        text
    )
    text = re.sub(r"</TabItem>", "", text)
    return text

# -------------------------
# LINK FIXER
# -------------------------

def fix_links(text, file_path: Path):
    def repl(m):
        path = m.group(1)
        anchor = m.group(2) or ""

        if path.startswith("http") or path.startswith("mailto:"):
            return m.group(0)

        target = DOCS / path.lstrip("/")

        # Попытка найти правильный файл
        if (target / "index.md").exists():
            new = path.lstrip("/") + "/index.md"
        elif target.with_suffix(".md").exists():
            new = path.lstrip("/") + ".md"
        else:
            # Пытаемся сделать относительным от текущего файла
            candidate = Path(os.path.relpath(target, start=file_path.parent))
            new = candidate.as_posix()

        return f"]({new}{anchor})"

    return re.sub(r"\]\(/([^)\#]+)(#[^)]+)?\)", repl, text)

# -------------------------
# IMAGE PATH FIX
# -------------------------

def fix_images(text, file_path: Path):
    """
    Исправляет пути к картинкам, делая их относительными от текущего Markdown-файла.
    """
    def repl(m):
        alt_text = m.group(1)
        img_path = m.group(2)

        if img_path.startswith("/assets/"):
            rel = Path(img_path.lstrip("/"))
            rel_path = Path(os.path.relpath(DOCS / rel, start=file_path.parent))
            return f"![{alt_text}]({rel_path.as_posix()})"
        return m.group(0)

    return re.sub(r"!\[(.*?)\]\((.*?)\)", repl, text)

# -------------------------
# HTML CRASH GUARD
# -------------------------

def html_crash_guard(text):
    text = re.sub(r"<details>.*?</details>", "", text, flags=re.S)
    text = re.sub(r"<summary>.*?</summary>", "", text, flags=re.S)
    text = text.replace("<br>", "\n")
    text = text.replace("<br/>", "\n")
    return text

# -------------------------
# FULL FILE PIPELINE
# -------------------------

def process_file(p: Path):
    text = read_text_safe(p)
    text = strip_frontmatter(text)
    text = clean_mdx(text)
    text = convert_admonitions(text)
    text = convert_tabs(text)
    text = fix_links(text, p)
    text = fix_images(text, p)
    text = html_crash_guard(text)
    write_text_safe(p, text)

# -------------------------
# MDX → MD RENAME
# -------------------------

def convert_mdx_files():
    for mdx in DOCS.rglob("*.mdx"):
        md = mdx.with_suffix(".md")
        mdx.rename(md)
        print("MDX→MD:", md)

# -------------------------
# CATEGORY → NAV
# -------------------------

def build_nav():
    nav = []
    for cat in sorted(DOCS.rglob("_category_.json")):
        data = json.loads(read_text_safe(cat))
        title = data.get("label", cat.parent.name)

        pages = []
        for md in sorted(cat.parent.glob("*.md")):
            rel = str(md.relative_to(DOCS)).replace("\\", "/")
            if md.name == "index.md":
                pages.insert(0, {"Overview": rel})
            else:
                name = md.stem.replace("-", " ").title()
                pages.append({name: rel})

        if pages:
            nav.append({title: pages})

    return nav

# -------------------------
# UPDATE MKDOCS.YML
# -------------------------

def update_mkdocs(nav):
    if MKDOCS.exists():
        cfg = yaml.safe_load(read_text_safe(MKDOCS)) or {}
    else:
        cfg = {}

    cfg["site_name"] = "Open WebUI Docs"

    cfg["theme"] = {
        "name": "material",
        "features": [
            "navigation.sections",
            "navigation.expand",
            "navigation.instant"
        ]
    }

    cfg["markdown_extensions"] = [
        "admonition",
        "pymdownx.details",
        "pymdownx.superfences",
        "pymdownx.tabbed"
    ]

    cfg["plugins"] = ["search"]
    cfg["nav"] = nav

    write_text_safe(MKDOCS, yaml.dump(cfg, allow_unicode=True, sort_keys=False))

# -------------------------
# MAIN
# -------------------------

def main():
    print("=== MDX → MD ===")
    convert_mdx_files()

    print("=== Processing Markdown ===")
    for md in DOCS.rglob("*.md"):
        process_file(md)

    print("=== Build nav ===")
    nav = build_nav()

    print("=== Update mkdocs.yml ===")
    update_mkdocs(nav)

    print("\nDONE ✅")

if __name__ == "__main__":
    main()
