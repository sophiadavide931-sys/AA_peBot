import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Get token
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    print("ERROR: BOT_TOKEN not set!")
    exit(1)

# Command handlers
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🤖 **PipBot is LIVE!**\n\n"
        "Commands:\n"
        "/calc - P&L calculator\n"
        "/risk - Risk/Reward\n"
        "/fib - Fibonacci levels\n"
        "/help - Show help",
        parse_mode="Markdown"
    )

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text(
        "📊 **Commands:**\n"
        "/calc [entry] [exit] - P&L\n"
        "/risk [entry] [stop] [target] - R:R\n"
        "/fib [high] [low] - Fibonacci"
    )

def calc(update: Update, context: CallbackContext):
    try:
        args = context.args
        if len(args) < 2:
            update.message.reply_text("Usage: /calc [entry] [exit]")
            return
        
        entry = float(args[0])
        exit_price = float(args[1])
        pnl = (exit_price - entry) * 10000
        
        update.message.reply_text(
            f"📈 P&L: {pnl:.2f} pips"
        )
    except:
        update.message.reply_text("❌ Invalid numbers!")

def risk(update: Update, context: CallbackContext):
    try:
        args = context.args
        if len(args) < 3:
            update.message.reply_text("Usage: /risk [entry] [stop] [target]")
            return
        
        entry = float(args[0])
        stop = float(args[1])
        target = float(args[2])
        
        risk = abs(entry - stop)
        reward = abs(target - entry)
        rr = reward / risk if risk > 0 else 0
        
        update.message.reply_text(
            f"📊 R:R = {rr:.2f}:1\n"
            f"Risk: {risk:.2f}\n"
            f"Reward: {reward:.2f}"
        )
    except:
        update.message.reply_text("❌ Invalid numbers!")

def fib(update: Update, context: CallbackContext):
    try:
        args = context.args
        if len(args) < 2:
            update.message.reply_text("Usage: /fib [high] [low]")
            return
        
        high = float(args[0])
        low = float(args[1])
        diff = high - low
        
        levels = {
            "0.0%": high,
            "23.6%": high - diff * 0.236,
            "38.2%": high - diff * 0.382,
            "50.0%": high - diff * 0.5,
            "61.8%": high - diff * 0.618,
            "100%": low
        }
        
        msg = "📐 Fibonacci:\n"
        for level, price in levels.items():
            msg += f"{level}: {price:.4f}\n"
        
        update.message.reply_text(msg)
    except:
        update.message.reply_text("❌ Invalid numbers!")

def main():
    print("🤖 Starting PipBot...")
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # Add handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("calc", calc))
    dp.add_handler(CommandHandler("risk", risk))
    dp.add_handler(CommandHandler("fib", fib))
    
    print("✅ Bot is running! Sending /start to test...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
