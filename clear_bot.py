#!/usr/bin/env python3
"""
Script để clear Telegram bot state và test connection
"""
import os
import asyncio
import sys
from dotenv import load_dotenv
import telegram

# Load environment
load_dotenv()

async def clear_bot_state():
    """Clear bot state và test connection"""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("❌ Thiếu TELEGRAM_BOT_TOKEN trong .env")
        return False
    
    try:
        # Tạo bot instance đơn giản
        bot = telegram.Bot(token=token)
        
        # Test connection
        print("🔄 Đang test connection...")
        me = await bot.get_me()
        print(f"✅ Bot connected: @{me.username}")
        
        # Clear pending updates (để tránh conflict)
        print("🔄 Đang clear pending updates...")
        updates = await bot.get_updates(timeout=1, limit=100)
        
        if updates:
            # Get offset của update cuối cùng
            last_update_id = updates[-1].update_id
            # Clear tất cả updates cũ
            await bot.get_updates(offset=last_update_id + 1, timeout=1)
            print(f"✅ Đã clear {len(updates)} pending updates")
        else:
            print("✅ Không có pending updates")
        
        print("🎉 Bot state đã được clear thành công!")
        return True
        
    except telegram.error.Conflict as e:
        print(f"❌ Conflict error: {e}")
        print("💡 Có bot instance khác đang chạy")
        return False
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False

def main():
    """Main function"""
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    print("🚀 Telegram Bot State Cleaner")
    print("=" * 40)
    
    result = asyncio.run(clear_bot_state())
    
    if result:
        print("\n✅ Bây giờ bạn có thể chạy bot chính:")
        print("   python app.py")
    else:
        print("\n❌ Không thể clear state. Hãy:")
        print("   1. Đợi 2-3 phút")
        print("   2. Kiểm tra các IDE/terminal khác")
        print("   3. Restart máy tính nếu cần")

if __name__ == "__main__":
    main()