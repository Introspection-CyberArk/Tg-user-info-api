import ijson
import sqlite3
import os

JSON_PATH = 'data/Telegram_70M.json'
DB_PATH = 'telegram_users.db'

print("📖 Converting 7GB JSON to SQLite...")
print("⏳ This will take 10-20 minutes but only needs to run once!")

# Create database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        account_id TEXT,
        phone TEXT,
        username TEXT,
        first_name TEXT,
        last_name TEXT
    )
''')

# Create indexes for fast searching
cursor.execute('CREATE INDEX IF NOT EXISTS idx_phone ON users(phone)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_username ON users(username)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_name ON users(first_name, last_name)')

# Stream JSON and insert
count = 0
with open(JSON_PATH, 'rb') as f:
    parser = ijson.items(f, 'item')
    
    for item in parser:
        cursor.execute(
            "INSERT INTO users (account_id, phone, username, first_name, last_name) VALUES (?, ?, ?, ?, ?)",
            (
                item.get('account_id'),
                item.get('phone'),
                item.get('username'),
                item.get('first_name', ''),
                item.get('last_name', '')
            )
        )
        count += 1
        
        if count % 100000 == 0:
            conn.commit()
            print(f"📊 Inserted {count} users...")

conn.commit()
print(f"✅ Done! {count} users in database")
conn.close()