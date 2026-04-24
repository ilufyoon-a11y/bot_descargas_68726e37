import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)
import yt_dlp

TOKEN = os.environ.get("TOKEN")

# 🌸 /start bonito
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "🌸 Hola!! 🐰✨\n\n"
        "Pásame un link y te ayudo a descargar:\n\n"
        "🎬 Video\n🎧 Audio\n\n"
        "Solo pega el link 💖"
    )

    foto = "https://i.pinimg.com/originals/3f/26/57/3f26577ae86a98ed05fdf2e2a3d2a61d.gif"  # puedes cambiarla

    await update.message.reply_photo(photo=foto, caption=texto)


# 📩 Recibir link
async def recibir_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if "http" not in url:
        await update.message.reply_text("Eso no es un link 😭")
        return

    context.user_data["url"] = url

    botones = [
        [InlineKeyboardButton("🎬 Video", callback_data="video")],
        [InlineKeyboardButton("🎧 Audio", callback_data="audio")],
    ]

    await update.message.reply_text(
        "✨ ¿Qué quieres descargar?",
        reply_markup=InlineKeyboardMarkup(botones),
    )


# 🎛️ Botones
async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    url = context.user_data.get("url")

    if not url:
        await query.edit_message_text("No hay link 😭")
        return

    # 🎬 VIDEO
    if query.data == "video":
        botones_calidad = [
            [InlineKeyboardButton("360p", callback_data="360")],
            [InlineKeyboardButton("480p", callback_data="480")],
        ]

        await query.edit_message_text(
            "🎬 Elige calidad:",
            reply_markup=InlineKeyboardMarkup(botones_calidad),
        )

    # 🎧 AUDIO
    elif query.data == "audio":
        await query.edit_message_text("🎧 Descargando audio...")

        try:
            ydl_opts = {
                'format': 'bestaudio',
                'outtmpl': 'audio.%(ext)s',
                'quiet': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            for file in os.listdir():
                if file.startswith("audio."):
                    with open(file, "rb") as f:
                        await query.message.reply_audio(f)
                    os.remove(file)
                    return

        except:
            await fallo(query)


# 🎬 DESCARGA VIDEO CON CALIDAD
async def calidad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    url = context.user_data.get("url")
    calidad = query.data

    await query.edit_message_text(f"🎬 Descargando en {calidad}p... ⏳")

    try:
        ydl_opts = {
            'format': f'best[height<={calidad}]',
            'outtmpl': 'video.%(ext)s',
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        for file in os.listdir():
            if file.startswith("video."):
                with open(file, "rb") as f:
                    await query.message.reply_video(f)
                os.remove(file)
                return

    except:
        await fallo(query)


# 😭 MENSAJE BONITO CUANDO FALLA
async def fallo(query):
    texto = (
        "😭 nooo TT\n\n"
        "Ese video no se pudo descargar 💔\n"
        "pero aquí tienes el link:\n"
    )

    foto = "https://i.pinimg.com/originals/02/14/38/0214384a806a47f811fb8cd535fb89cc.gif"

    await query.message.reply_photo(
        photo=foto,
        caption=texto
    )


# 🚀 APP
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_link))
app.add_handler(CallbackQueryHandler(botones, pattern="^(video|audio)$"))
app.add_handler(CallbackQueryHandler(calidad, pattern="^(360|480)$"))

app.run_polling()
