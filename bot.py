import os
import telebot
import time

# Get token from environment
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    print("❌ ERROR: BOT_TOKEN environment variable not set!")
    exit(1)

# Initialize bot
bot = telebot.TeleBot(TOKEN)
print(f"✅ Bot started with token: {TOKEN[:10]}...")

@bot.message_handler(commands=['start'])
def send_start(message):
    print(f"📩 /start from {message.from_user.first_name}")
    bot.reply_to(message, "✅ PipBot is LIVE! Commands:\n/calc\n/risk\n/fib\n/help")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "📊 Commands:\n/calc [entry] [exit]\n/risk [entry] [stop] [target]\n/fib [high] [low]")

@bot.message_handler(commands=['calc'])
def calc_pnl(message):
    try:
        args = message.text.split()[1:]
        if len(args) < 2:
            bot.reply_to(message, "Usage: /calc [entry] [exit]")
            return
        
        entry = float(args[0])
        exit_price = float(args[1])
        pnl = (exit_price - entry) * 10000
        
        bot.reply_to(message, f"📈 P&L: {pnl:.2f} pips")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: Use numbers only!")

@bot.message_handler(commands=['risk'])
def risk_reward(message):
    try:
        args = message.text.split()[1:]
        if len(args) < 3:
            bot.reply_to(message, "Usage: /risk [entry] [stop] [target]")
            return
        
        entry = float(args[0])
        stop = float(args[1])
        target = float(args[2])
        
        risk = abs(entry - stop)
        reward = abs(target - entry)
        rr = reward / risk if risk > 0 else 0
        
        bot.reply_to(message, f"📊 R:R = {rr:.2f}:1\nRisk: {risk:.2f}\nReward: {reward:.2f}")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: Use numbers only!")

@bot.message_handler(commands=['fib'])
def fibonacci(message):
    try:
        args = message.text.split()[1:]
        if len(args) < 2:
            bot.reply_to(message, "Usage: /fib [high] [low]")
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
        
        bot.reply_to(message, msg)
    except Exception as e:
        bot.reply_to(message, f"❌ Error: Use numbers only!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "🤖 Use /start for commands")

# Keep polling
if __name__ == "__main__":
    try:
        print("🔄 Bot polling started...")
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"❌ Error: {e}")
        time.sleep(5)
