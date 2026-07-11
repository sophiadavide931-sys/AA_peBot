import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Get token from environment
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    print("ERROR: BOT_TOKEN environment variable not set!")
    exit(1)

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 **PipBot is alive!**\n\n"
        "Commands:\n"
        "/calc - P&L calculator\n"
        "/risk - Risk/Reward ratio\n"
        "/fib - Fibonacci levels\n"
        "/pipvalue - Pip value calculator\n"
        "/help - Show help",
        parse_mode="Markdown"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 **PipBot Commands**\n\n"
        "/calc [entry] [exit] [size] - P&L\n"
        "/risk [entry] [stop] [target] - Risk/Reward\n"
        "/fib [high] [low] - Fibonacci levels\n"
        "/pipvalue [lots] [pip] - Pip value"
    )

async def calc_pnl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) < 2:
            await update.message.reply_text("Usage: /calc [entry] [exit] [size]")
            return
            
        entry = float(args[0])
        exit_price = float(args[1])
        size = float(args[2]) if len(args) > 2 else 1.0
        
        pnl = (exit_price - entry) * size
        pnl_pct = ((exit_price - entry) / entry) * 100
        
        await update.message.reply_text(
            f"📈 **P&L Result**\n\n"
            f"Entry: {entry}\n"
            f"Exit: {exit_price}\n"
            f"Size: {size}\n"
            f"P&L: {pnl:.2f}\n"
            f"Change: {pnl_pct:.2f}%",
            parse_mode="Markdown"
        )
    except ValueError:
        await update.message.reply_text("❌ Use numbers only!")

async def risk_reward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) < 3:
            await update.message.reply_text("Usage: /risk [entry] [stop] [target]")
            return
            
        entry = float(args[0])
        stop = float(args[1])
        target = float(args[2])
        
        risk = abs(entry - stop)
        reward = abs(target - entry)
        rr = reward / risk if risk > 0 else 0
        
        await update.message.reply_text(
            f"📊 **Risk/Reward**\n\n"
            f"Entry: {entry}\n"
            f"Stop: {stop}\n"
            f"Target: {target}\n"
            f"Risk: {risk:.2f}\n"
            f"Reward: {reward:.2f}\n"
            f"R:R: **{rr:.2f}:1**",
            parse_mode="Markdown"
        )
    except ValueError:
        await update.message.reply_text("❌ Use numbers only!")

async def fibonacci(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) < 2:
            await update.message.reply_text("Usage: /fib [high] [low]")
            return
            
        high = float(args[0])
        low = float(args[1])
        diff = high - low
        
        levels = {
            "0%": high,
            "23.6%": high - diff * 0.236,
            "38.2%": high - diff * 0.382,
            "50%": high - diff * 0.5,
            "61.8%": high - diff * 0.618,
            "78.6%": high - diff * 0.786,
            "100%": low
        }
        
        msg = "📐 **Fibonacci Levels**\n\n"
        for level, price in levels.items():
            msg += f"{level}: {price:.4f}\n"
            
        await update.message.reply_text(msg, parse_mode="Markdown")
    except ValueError:
        await update.message.reply_text("❌ Use numbers only!")

async def pip_value(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) < 2:
            await update.message.reply_text("Usage: /pipvalue [lots] [pip]")
            return
            
        lots = float(args[0])
        pip = float(args[1])
        pip_value = lots * 100000 * pip
        
        await update.message.reply_text(
            f"💵 **Pip Value**\n\n"
            f"Lots: {lots}\n"
            f"Pip: {pip}\n"
            f"Value: ${pip_value:.2f}",
            parse_mode="Markdown"
        )
    except ValueError:
        await update.message.reply_text("❌ Use numbers only!")

# Main function
def main():
    app = Application.builder().token(TOKEN).build()
    
    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("calc", calc_pnl))
    app.add_handler(CommandHandler("risk", risk_reward))
    app.add_handler(CommandHandler("fib", fibonacci))
    app.add_handler(CommandHandler("pipvalue", pip_value))
    
    print("🤖 PipBot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
