from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import yt_dlp
import os

TOKEN = "TU_TOKEN_AQUI"

async def descargar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    await update.message.reply_text("Descargando... ?")

    try:
        ydl_opts = {
            'outtmpl': 'video.%(ext)s',
            'format': 'best[filesize<50M]'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        for file in os.listdir():
            if file.startswith("video."):
                with open(file, "rb") as f:
                    await update.message.reply_video(f)

                os.remove(file)
                break

    except:
        await update.message.reply_text("Error ??")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, descargar))
app.run_polling()