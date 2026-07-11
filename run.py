from bot import bot
import time

if __name__ == "__main__":
    print("🚀 PipBot is running...")
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"❌ Polling error: {e}")
        time.sleep(5)
