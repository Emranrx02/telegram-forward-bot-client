from telegram.ext import Updater, MessageHandler, Filters
from telegram import InputMediaPhoto, InputMediaVideo
import os
from dotenv import load_dotenv
load_dotenv()

# Load environment variables
BOT_TOKEN = os.environ['BOT_TOKEN']
SOURCE_CHAT_ID = int(os.environ['SOURCE_CHAT_ID'])
DEST_CHAT_ID = int(os.environ['DEST_CHAT_ID'])

def forward_message(update, context):
    print("✅ Message received:", update.message)
    message = update.message

    if message.chat.id != SOURCE_CHAT_ID:
        print("⛔ Ignored (not from source group)")
        return

    try:
        if message.text:
            print("✉️ Forwarding text...")
            context.bot.send_message(chat_id=DEST_CHAT_ID, text=message.text)

        elif message.photo:
            print("🖼 Forwarding photo...")
            photo = message.photo[-1].file_id
            caption = message.caption or ""
            context.bot.send_photo(chat_id=DEST_CHAT_ID, photo=photo, caption=caption)

        elif message.video:
            print("🎥 Forwarding video...")
            video = message.video.file_id
            caption = message.caption or ""
            context.bot.send_video(chat_id=DEST_CHAT_ID, video=video, caption=caption)

        else:
            print("🔁 Using fallback forward...")
            message.forward(chat_id=DEST_CHAT_ID)

    except Exception as e:
        print("❗ Error:", e)

def main():
    print("🤖 Bot starting...")
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.all, forward_message))
    updater.start_polling()
    print("🚀 Bot polling started...")
    updater.idle()

if __name__ == '__main__':
    main()
