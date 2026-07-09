import json
import os
import random
import re
import sys
import time

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

import database
from scraper import extract_tid

CACHE_PATH = "geocode_cache.json"
ADELAIDE_VIEWBOX = ((-35.35, 138.4), (-34.5, 139.0))


def clean_price(price_str):
    if not price_str:
        return None
    match = re.search(r"\d+", price_str)
    if not match:
        return None
    return int(match.group())


def _load_cache():
    if not os.path.exists(CACHE_PATH):
        return {}
    with open(CACHE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_cache(cache):
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def geocode(anchor):
    if anchor is None:
        return None

    cache = _load_cache()
    if anchor in cache:
        cached = cache[anchor]
        return tuple(cached) if cached is not None else None

    geolocator = Nominatim(user_agent="rentmapau-importer")
    location = geolocator.geocode(
        anchor,
        country_codes="au",
        viewbox=ADELAIDE_VIEWBOX,
        bounded=True,
    )
    time.sleep(1)

    if location is None:
        cache[anchor] = None
        _save_cache(cache)
        return None

    result = (location.latitude, location.longitude)
    cache[anchor] = list(result)
    _save_cache(cache)
    return result


def build_listing(data):
    description = data["描述"] or ""
    if data.get("missing_fields"):
        missing = ",".join(data["missing_fields"])
        description += f"\n\n[抓取备注:以下字段原帖未提及,已填默认值:{missing}]"

    coords = geocode(data.get("location_anchor"))
    if coords is None:
        latitude, longitude = None, None
    else:
        latitude = coords[0] + random.uniform(-0.0005, 0.0005)
        longitude = coords[1] + random.uniform(-0.0005, 0.0005)

    return {
        "标题": data["标题"],
        "区域": data["区域"],
        "价格": clean_price(data["价格"]),
        "房型": data["房型"],
        "描述": description,
        "图片": ",".join(data["图片"]),
        "联系人": data.get("联系人") or "",
        "电话": data.get("电话") or "",
        "微信": data.get("微信") or "",
        "是否包bill": data["是否包bill"],
        "是否带家具": data["是否带家具"],
        "纬度": latitude,
        "经度": longitude,
        "status": "pending",
        "source_url": data["source_url"],
    }


def main():
    if len(sys.argv) != 2:
        sys.exit("用法: python import_listing.py extracted/<tid>.json")

    json_path = sys.argv[1]
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if data.get("status") == "location_unresolvable":
        sys.exit("该帖位置不可解析,跳过导入")

    tid = extract_tid(data["source_url"])

    supabase = database.get_supabase_client()
    existing = (
        supabase
        .table("listings")
        .select("id")
        .like("source_url", f"%tid={tid}%")
        .execute()
    )
    if existing.data:
        sys.exit(f"tid={tid} 已存在于数据库中 (id={existing.data[0]['id']}),跳过导入")

    listing = build_listing(data)
    database.insert_listing(listing)

    print("导入成功:")
    print(f"  标题: {listing['标题']}")
    print(f"  区域: {listing['区域']}")
    print(f"  价格: {listing['价格']}")
    print(f"  房型: {listing['房型']}")
    print(f"  纬度/经度: {listing['纬度']}, {listing['经度']}")
    print(f"  联系人/电话/微信: {listing['联系人']} / {listing['电话']} / {listing['微信']}")
    print(f"  status: {listing['status']}")


if __name__ == "__main__":
    main()
