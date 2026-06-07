import sqlite3
import time

DB_PATH = 'telegram_users.db'

def get_total():
    """Get total number of users"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    total = cursor.fetchone()[0]
    conn.close()
    return total

def search_by_username(username):
    """Search by username (fastest - uses index)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    start = time.time()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username.lower(),))
    result = cursor.fetchone()
    elapsed = time.time() - start
    conn.close()
    return result, elapsed

def search_by_phone(phone):
    """Search by phone number (fast - uses index)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    start = time.time()
    cursor.execute("SELECT * FROM users WHERE phone = ?", (phone,))
    result = cursor.fetchone()
    elapsed = time.time() - start
    conn.close()
    return result, elapsed

def search_by_name(name):
    """Search by name (slower - no index)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    start = time.time()
    cursor.execute(
        "SELECT * FROM users WHERE first_name LIKE ? OR last_name LIKE ? LIMIT 10",
        (f'%{name}%', f'%{name}%')
    )
    results = cursor.fetchall()
    elapsed = time.time() - start
    conn.close()
    return results, elapsed

# Main menu
def show_menu():
    print("\n" + "=" * 50)
    print("🔍 TELEGRAM USER DATABASE SEARCH")
    print("=" * 50)
    print(f"📊 Total users: {get_total():,}")
    print("-" * 50)
    print("1. Search by Username (fastest)")
    print("2. Search by Phone Number (fast)")
    print("3. Search by Name (slower)")
    print("4. Exit")
    print("-" * 50)

def main():
    while True:
        show_menu()
        choice = input("\n👉 Choose option (1-4): ").strip()
        
        if choice == '1':
            username = input("Enter username (e.g., MorozS): ").strip()
            if not username:
                print("❌ Username cannot be empty!")
                continue
            
            print(f"\n🔎 Searching for '{username}'...")
            result, elapsed = search_by_username(username)
            
            if result:
                print("\n✅ RECORD FOUND!")
                print("=" * 40)
                print(f"📱 Phone:     {result[1]}")
                print(f"👤 Username:  @{result[2]}")
                print(f"📛 First Name: {result[3]}")
                print(f"📛 Last Name:  {result[4]}")
                print(f"🆔 Account ID: {result[0]}")
                print("=" * 40)
                print(f"⏱️  Search time: {elapsed:.3f} seconds")
            else:
                print(f"\n❌ Username '{username}' not found in database")
                print(f"⏱️  Search time: {elapsed:.3f} seconds")
        
        elif choice == '2':
            phone = input("Enter phone number (e.g., 79254677980): ").strip()
            if not phone:
                print("❌ Phone number cannot be empty!")
                continue
            
            print(f"\n🔎 Searching for '{phone}'...")
            result, elapsed = search_by_phone(phone)
            
            if result:
                print("\n✅ RECORD FOUND!")
                print("=" * 40)
                print(f"📱 Phone:     {result[1]}")
                print(f"👤 Username:  @{result[2]}")
                print(f"📛 First Name: {result[3]}")
                print(f"📛 Last Name:  {result[4]}")
                print(f"🆔 Account ID: {result[0]}")
                print("=" * 40)
                print(f"⏱️  Search time: {elapsed:.3f} seconds")
            else:
                print(f"\n❌ Phone '{phone}' not found in database")
                print(f"⏱️  Search time: {elapsed:.3f} seconds")
        
        elif choice == '3':
            name = input("Enter name to search (e.g., Morozov): ").strip()
            if not name:
                print("❌ Name cannot be empty!")
                continue
            
            print(f"\n🔎 Searching for names containing '{name}'...")
            print("⏳ This may take 10-30 seconds...")
            results, elapsed = search_by_name(name)
            
            if results:
                print(f"\n✅ FOUND {len(results)} RESULTS!")
                print("=" * 40)
                for i, row in enumerate(results, 1):
                    print(f"\n{i}. 👤 {row[3]} {row[4]}")
                    print(f"   📱 @{row[2]}")
                    print(f"   📞 {row[1]}")
                print("=" * 40)
                print(f"⏱️  Search time: {elapsed:.3f} seconds")
            else:
                print(f"\n❌ No names containing '{name}' found")
                print(f"⏱️  Search time: {elapsed:.3f} seconds")
        
        elif choice == '4':
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice! Please enter 1, 2, 3, or 4")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()