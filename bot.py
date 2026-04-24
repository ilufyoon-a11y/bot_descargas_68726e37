import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import yt_dlp

TOKEN = os.environ.get("TOKEN")

async def descargar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    # 🔒 Validar que sea un link
    if "http" not in url:
        await update.message.reply_text("Eso no es un link 😭")
        return

    await update.message.reply_text("Descargando... ⏳")

    try:
        ydl_opts = {
            'outtmpl': 'video.%(ext)s',
            'format': 'best[height<=480]',  # evita archivos pesados
            'noplaylist': True,
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # 📤 Enviar archivo
        for file in os.listdir():
            if file.startswith("video."):
                with open(file, "rb") as f:
                    await update.message.reply_video(f)

                os.remove(file)
                break

    except Exception as e:
        await update.message.reply_text("No se pudo descargar 😓 prueba otro video")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, descargar))

app.run_polling()
