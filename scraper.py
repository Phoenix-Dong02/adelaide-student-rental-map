import json
import os
import re
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")
from urllib.parse import urljoin, urlparse, parse_qs

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.adelaidebbs.com/bbs/"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)


def extract_tid(url: str) -> str:
    query = parse_qs(urlparse(url).query)
    tid = query.get("tid", [None])[0]
    if not tid:
        sys.exit("这不是一个帖子链接")
    return tid


def fetch_thread(url: str) -> str:
    resp = requests.get(url, headers={"User-Agent": USER_AGENT})
    resp.raise_for_status()
    resp.encoding = "gbk"
    return resp.text


def clean_thread(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    subject = soup.find(id="thread_subject")
    if subject and subject.get_text(strip=True):
        title = subject.get_text(strip=True)
    elif soup.title and soup.title.get_text(strip=True):
        title = soup.title.get_text(strip=True)
    else:
        title = None

    post_elem = soup.find(id=re.compile(r"^postmessage_\d+$"))
    post_text = None
    image_urls = []
    if post_elem is not None:
        post_text = "\n".join(
            line.strip()
            for line in post_elem.get_text(separator="\n").splitlines()
            if line.strip()
        )

        seen = set()
        container = post_elem.find_parent("div", class_="pcb") or post_elem
        for img in container.find_all("img"):
            path = img.get("zoomfile") or img.get("file")
            if not path or path in seen:
                continue
            seen.add(path)
            image_urls.append(urljoin(BASE_URL, path))

    return {
        "title": title,
        "post_text": post_text,
        "image_urls": image_urls,
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("用法: python scraper.py \"帖子完整URL\"")

    thread_url = sys.argv[1]
    tid = extract_tid(thread_url)
    html = fetch_thread(thread_url)
    result = clean_thread(html)
    result["source_url"] = thread_url
    result["tid"] = tid
    result["scraped_at"] = datetime.now().isoformat()

    out_dir = "scraped"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{tid}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(json.dumps(result, ensure_ascii=False, indent=2))
