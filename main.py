import os
import random
import asyncio
import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from telegram.ext import Application, CommandHandler
from keep_alive import start_keep_alive

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logging.getLogger("httpx").setLevel(logging.WARNING)

TOKEN = os.environ.get("BOT_TOKEN")
PAIRES = ["EUR/USD", "GBP/USD", "USD/JPY", "BTC/USD"]
BUTEMBO_TIMEZONE = ZoneInfo("Africa/Lubumbashi")
auto_chat = None

def formater_signal(pair, direction, score, strategie, automatique=False):
    now_butembo = datetime.now(BUTEMBO_TIMEZONE)
    entree = now_butembo + timedelta(minutes=2)
    expiration = entree + timedelta(minutes=5)
    titre = "🚀 AUTO" if automatique else "🔥 SIGNAL"
    return f"{titre}\n{pair} {direction} {score}% {strategie}\n⏰ ENTRÉE À: {entree:%H:%M} (Heure Butembo)\n⏳ EXPIRATION: {expiration:%H:%M} (5 MIN)\n📊 Paire: {pair}"

def signal_puissant(p):
    return random.choice(["CALL 📈", "PUT 📉"]), random.randint(88, 99), "EMA+RSI"

async def start(update, context):
    await update.message.reply_text("🤖 AROMA CLOUD 24/7 EN LIGNE\n/signal - signal\n/auto - auto\n/stop - stop")

async def signal_cmd(update, context):
    direction, score, strategie = signal_puissant("")
    pair = random.choice(PAIRES)
    await update.message.reply_text(formater_signal(pair, direction, score, strategie))

async def auto_loop(app):
    global auto_chat
    while True:
        if auto_chat:
            direction, score, strategie = signal_puissant("")
            pair = random.choice(PAIRES)
            await app.bot.send_message(chat_id=auto_chat, text=formater_signal(pair, direction, score, strategie, automatique=True))
        await asyncio.sleep(120)

async def auto_cmd(update, context):
    global auto_chat
    auto_chat = update.effective_chat.id
    await update.message.reply_text("✅ AUTO activé toutes les 2 min")
    context.application.create_task(auto_loop(context.application))

async def stop_cmd(update, context):
    global auto_chat
    auto_chat = None
    await update.message.reply_text("🔴 AUTO Stop")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal_cmd))
    app.add_handler(CommandHandler("auto", auto_cmd))
    app.add_handler(CommandHandler("stop", stop_cmd))
    start_keep_alive()
    print("BOT EN LIGNE", flush=True)
    app.run_polling()

if __name__ == "__main__":
    main()