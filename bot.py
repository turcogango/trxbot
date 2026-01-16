import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

ADDRESS = "TSjQYavgJBGPr8iV3zH7qo1bx927qKVMwA"
API_URL = "https://apilist.tronscan.org/api/account"


async def tether(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("⏳ Hesaplanıyor...")

        r = requests.get(API_URL, params={"address": ADDRESS}, timeout=10)
        data = r.json()

        trx_balance = data.get("balance", 0) / 1_000_000

        usdt_balance = 0.0
        for t in data.get("trc20token_balances", []):
            if t.get("tokenId") == "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t":
                usdt_balance = int(t.get("balance", 0)) / 1_000_000
                break

        text = (
            f"📍 {ADDRESS}\n\n"
            f"⭐️ TRX: {trx_balance:,.2f} TRX\n"
            f"⭐️ USDT: ${usdt_balance:,.2f}"
        )

        await update.message.reply_text(text)

    except Exception as e:
        print(e)
        await update.message.reply_text("❌ Veri okunamadı")


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("tether", tether))
    print("✅ Bot çalışıyor...")
    app.run_polling()


if __name__ == "__main__":
    main()
