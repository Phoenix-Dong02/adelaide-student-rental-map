import json
import sys
import os
from datetime import datetime
from pathlib import Path

import anthropic

sys.stdout.reconfigure(encoding="utf-8")

RULES_PATH = Path.home() / ".claude/skills/adelaidebbs-rental-extract/SKILL.md"

JSON_ONLY_INSTRUCTION = (
    "\n\n你的回复必须是且仅是一个 JSON 对象。不要任何解释、"
    "前言、markdown 代码块围栏。第一个字符必须是 {。"
)


_IMAGE_BULLET = (
    '- **图片**: within the same `postmessage_NNNNNNN` block (and the attachment\n'
    '  list right after it), find `<img ... zoomfile="data/attachment/forum/...">`\n'
    '  tags — `zoomfile` (or `file`) holds the path to the actual full-resolution\n'
    '  image, not the `src` attribute (which is usually a `none.gif` placeholder\n'
    '  swapped in by JS). Grep the decoded file for `zoomfile="` to collect every\n'
    "  path. Resolve each relative path against the thread URL's origin, e.g.\n"
    '  `data/attachment/forum/202606/29/xxxxx.jpeg` →\n'
    '  `https://www.adelaidebbs.com/bbs/data/attachment/forum/202606/29/xxxxx.jpeg`.\n'
    '  Return as a plain list of absolute URLs — do not fetch, download, or\n'
    '  re-host the images.\n'
)


def _strip_image_field(rules: str) -> str:
    rules = rules.replace(_IMAGE_BULLET, "")
    rules = rules.replace('    "图片": [],\n', "")
    rules = rules.replace('  "图片": ["...", "..."],\n', "")
    rules = rules.replace(
        "Use `null` for any field that wasn't found (and `[]` for `图片`/`missing_fields`\n"
        "if empty).",
        "Use `null` for any field that wasn't found (and `[]` for `missing_fields`\n"
        "if empty).",
    )
    return rules


def load_rules() -> str:
    if not RULES_PATH.exists():
        sys.exit(f"找不到规则文件: {RULES_PATH}")
    rules = RULES_PATH.read_text(encoding="utf-8")
    return _strip_image_field(rules)


def extract(scraped: dict) -> dict:
    client = anthropic.Anthropic()

    user_message = (
        f"标题:{scraped['title']}\n"
        f"正文:{scraped['post_text']}\n"
        f"source_url:{scraped['source_url']}"
    )

    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=2000,
        system=load_rules() + JSON_ONLY_INSTRUCTION,
        messages=[{"role": "user", "content": user_message}],
    )

    text = next(b.text for b in response.content if b.type == "text").strip()

    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        if text.endswith("```"):
            text = text.rsplit("```", 1)[0]
        text = text.strip()
        if text.startswith("json"):
            text = text[4:].strip()

    try:
        result = json.loads(text)
    except json.JSONDecodeError:
        sys.exit(f"模型返回的不是合法 JSON,原始回复如下:\n{text}")

    result["图片"] = scraped["image_urls"]
    result.setdefault("source_url", scraped["source_url"])

    return result


def main():
    if len(sys.argv) != 2:
        sys.exit('用法: python extractor.py scraped/1621656.json')

    scraped_path = Path(sys.argv[1])
    tid = scraped_path.stem

    with open(scraped_path, "r", encoding="utf-8") as f:
        scraped = json.load(f)

    result = extract(scraped)

    out_dir = "extracted"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{tid}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
