import pandas as pd
import sqlite3

def get_seed_dataframe():
    listings = [
        {
            "标题": "阿德莱德CBD 近大学女生双人间床位",
            "区域": "Adelaide CBD",
            "价格": 230,
            "房型": "合租",
            "纬度": -34.9285,
            "经度": 138.6007,
            "描述": "步行可到阿大，近Rundle Mall，适合预算有限学生。",
            "图片": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80",
            "联系人": "Amy",
            "电话": "0412 345 678",
            "微信": "amy-rent-cbd",
            "是否包bill": "是",
            "是否带家具": "是"
        },
        {
            "标题": "North Adelaide 独立Studio",
            "区域": "North Adelaide",
            "价格": 315,
            "房型": "Studio",
            "纬度": -34.9071,
            "经度": 138.5947,
            "描述": "安静安全，适合喜欢独立空间的学生。",
            "图片": "https://images.unsplash.com/photo-1484154218962-a197022b5858?auto=format&fit=crop&w=1200&q=80",
            "联系人": "Leo",
            "电话": "0433 222 111",
            "微信": "leo-studio-na",
            "是否包bill": "否",
            "是否带家具": "是"
        },
        {
            "标题": "Norwood 单间招租",
            "区域": "Norwood",
            "价格": 250,
            "房型": "单间",
            "纬度": -34.9212,
            "经度": 138.6346,
            "描述": "周边中餐多，生活方便，公交进城快。",
            "图片": "https://images.unsplash.com/photo-1494526585095-c41746248156?auto=format&fit=crop&w=1200&q=80",
            "联系人": "Daniel",
            "电话": "0422 666 444",
            "微信": "daniel-norwood-room",
            "是否包bill": "是",
            "是否带家具": "否"
        },
        {
            "标题": "Prospect 两室一厅整租",
            "区域": "Prospect",
            "价格": 320,
            "房型": "整租",
            "纬度": -34.8840,
            "经度": 138.5940,
            "描述": "适合情侣或朋友一起合租，生活氛围好。",
            "图片": "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=1200&q=80",
            "联系人": "Grace",
            "电话": "0411 888 555",
            "微信": "grace-prospect-home",
            "是否包bill": "否",
            "是否带家具": "是"
        },
        {
            "标题": "Mawson Lakes 便宜合租房",
            "区域": "Mawson Lakes",
            "价格": 185,
            "房型": "合租",
            "纬度": -34.8153,
            "经度": 138.6103,
            "描述": "价格低，适合预算敏感型学生。",
            "图片": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80",
            "联系人": "Kevin",
            "电话": "0400 111 222",
            "微信": "kevin-mawson-share",
            "是否包bill": "是",
            "是否带家具": "是"
        },
        {
            "标题": "burnside 便宜合租房",
            "区域": "burnside",
            "价格": 170,
            "房型": "合租",
            "纬度": -34.9497,
            "经度": 138.6530,
            "描述": "价格低，适合预算敏感型学生。",
            "图片": "images/IMG_3266.JPG",
            "联系人": "houbingtao",
            "电话": "0400 111 222",
            "微信": "houbingtao1974",
            "是否包bill": "否",
            "是否带家具": "是"
        }
    ]

    return pd.DataFrame(listings)


def get_dataframe():
    conn = sqlite3.connect("rent.db")
    df = pd.read_sql("SELECT * FROM listings", conn)
    conn.close()
    return df