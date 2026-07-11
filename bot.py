import os

TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    print("❌ BOT_TOKEN not set!")
    exit(1)

print(f"✅ Token found: {TOKEN[:10]}...")

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

def start(update: Update, context: CallbackContext):
    print(f"📩 Received /start from {update.effective_user.first_name}")
    update.message.reply_text("✅ PipBot is working!")

def main():
    print("🤖 Starting bot...")
    updater = Updater(TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler("start", start))
    print("✅ Bot is polling...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
