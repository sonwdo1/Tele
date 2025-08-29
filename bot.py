# bot.py
import os, asyncio, subprocess, sys, shlex
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Lấy BOT_TOKEN từ biến môi trường Railway
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Gõ /tool <dữ liệu> để chạy tool CLI.")

def run_cli(query: str) -> str:
    # Thay "--q" bằng đúng tham số tool của bạn
    cmd = f'{sys.executable} lbdxaov.py --q {shlex.quote(query)}'
    completed = subprocess.run(
        cmd, shell=True, text=True, capture_output=True, timeout=120
    )
    if completed.returncode != 0:
        return f"❌ Tool lỗi (code {completed.returncode}): {completed.stderr.strip()}"
    return completed.stdout.strip() or "(✅ Tool không trả output)"

async def tool(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Cú pháp: /tool <dữ liệu>")
        return

    query = " ".join(context.args)
    try:
        result = await asyncio.to_thread(run_cli, query)
    except Exception as e:
        result = f"❌ Lỗi khi chạy tool: {e}"
    await update.message.reply_text(result)

def main():
    if not TOKEN:
        raise RuntimeError("Thiếu BOT_TOKEN trong biến môi trường Railway")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tool", tool))
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()