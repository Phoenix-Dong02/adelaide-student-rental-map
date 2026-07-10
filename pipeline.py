import json
import os
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")

import scraper
import extractor
import import_listing


def _exit_message(exc) -> str:
    if isinstance(exc, SystemExit):
        return str(exc.code) if exc.code is not None else ""
    return str(exc)


def _fail(step: str, exc, produced: list):
    print(f"\n流程在 {step} 失败: {_exit_message(exc)}")
    if produced:
        print("已产出的中间文件:")
        for path in produced:
            print(f"  - {path}")
    else:
        print("尚未产出任何中间文件。")
    sys.exit(1)


def main():
    if len(sys.argv) != 2:
        sys.exit('用法: python pipeline.py "帖子完整URL"')

    thread_url = sys.argv[1]
    produced = []

    print("[1/3] 抓取中...")
    try:
        tid = scraper.extract_tid(thread_url)
        html = scraper.fetch_thread(thread_url)
        scraped = scraper.clean_thread(html)
        scraped["source_url"] = thread_url
        scraped["tid"] = tid
        scraped["scraped_at"] = datetime.now().isoformat()

        os.makedirs("scraped", exist_ok=True)
        scraped_path = os.path.join("scraped", f"{tid}.json")
        with open(scraped_path, "w", encoding="utf-8") as f:
            json.dump(scraped, f, ensure_ascii=False, indent=2)
        produced.append(scraped_path)
    except (Exception, SystemExit) as e:
        _fail("[1/3] 抓取", e, produced)
    print(f"[1/3] 抓取完成 -> {scraped_path}")

    print("[2/3] AI 提取中...")
    try:
        extracted = extractor.extract(scraped)
        os.makedirs("extracted", exist_ok=True)
        extracted_path = os.path.join("extracted", f"{tid}.json")
        with open(extracted_path, "w", encoding="utf-8") as f:
            json.dump(extracted, f, ensure_ascii=False, indent=2)
        produced.append(extracted_path)
    except (Exception, SystemExit) as e:
        _fail("[2/3] AI 提取", e, produced)
    print(f"[2/3] AI 提取完成 -> {extracted_path}")

    if extracted.get("status") == "location_unresolvable":
        print("\n警告: 该帖位置不可解析(status=location_unresolvable),流程终止。")
        print("已产出的中间文件:")
        for path in produced:
            print(f"  - {path}")
        sys.exit(1)

    print("[3/3] 入库中...")
    try:
        import_listing.run_import(extracted_path)
    except (Exception, SystemExit) as e:
        _fail("[3/3] 入库", e, produced)
    print("[3/3] 入库完成。")


if __name__ == "__main__":
    main()
