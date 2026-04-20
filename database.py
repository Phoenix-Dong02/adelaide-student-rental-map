import sqlite3

def get_connection():
    # Create a connection to the SQLite database
    return sqlite3.connect("rent.db")


def create_table():
    # Create the listings table if it does not exist
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS listings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        标题 TEXT,
        区域 TEXT,
        价格 INTEGER,
        房型 TEXT,
        纬度 REAL,
        经度 REAL,
        描述 TEXT,
        图片 TEXT,
        联系人 TEXT,
        电话 TEXT,
        微信 TEXT,
        是否包bill TEXT,
        是否带家具 TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_listing(listing):
    # Insert a new rental listing into the database
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO listings (
        标题, 区域, 价格, 房型, 纬度, 经度,
        描述, 图片, 联系人, 电话, 微信,
        是否包bill, 是否带家具
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        listing["标题"],
        listing["区域"],
        listing["价格"],
        listing["房型"],
        listing["纬度"],
        listing["经度"],
        listing["描述"],
        listing["图片"],
        listing["联系人"],
        listing["电话"],
        listing["微信"],
        listing["是否包bill"],
        listing["是否带家具"]
    ))

    conn.commit()
    conn.close()