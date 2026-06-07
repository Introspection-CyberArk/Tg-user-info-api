import ijson
import os

JSON_PATH = 'data/Telegram_70M.json'

print("📖 Streaming Telegram user database (7GB file)...")
print("⏳ This will take 5-10 minutes...")

def load_users_stream():
    """Stream JSON array without loading everything into memory"""
    
    if not os.path.exists(JSON_PATH):
        print(f"❌ Error: {JSON_PATH} not found!")
        return []
    
    users = []
    
    # Use ijson to stream the array
    with open(JSON_PATH, 'rb') as f:
        # Parse each item in the array one by one
        parser = ijson.items(f, 'item')
        
        count = 0
        for item in parser:
            user = {
                'account_id': item.get('account_id'),
                'phone': item.get('phone'),
                'username': item.get('username'),
                'first_name': item.get('first_name', ''),
                'last_name': item.get('last_name', '')
            }
            users.append(user)
            count += 1
            
            # Progress update every 100,000 users
            if count % 100000 == 0:
                print(f"📊 Loaded {count} users...")
            
            # Optional: Stop after certain number for testing
            # if count >= 100000:
            #     print("🛑 Stopping at 100,000 users (remove this limit later)")
            #     break
    
    print(f"✅ Loaded {len(users)} users!")
    return users

# Load users
USERS = load_users_stream()