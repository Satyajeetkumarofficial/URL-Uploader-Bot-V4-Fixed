import os
from plugins.config import Config
from pyrogram import Client, filters
from threading import Thread
from flask import Flask
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

# Flask setup
flask_app = Flask('')

@flask_app.route('/')
def home():
    return "Bot is alive", 200

def run_flask():
    flask_app.run(host='0.0.0.0', port=8080)

Thread(target=run_flask).start()

# Pyrogram Client with plugins
plugins = dict(root="plugins")
bot = Client(
    "UploaderXNTBot",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    plugins=plugins
)

# Create download directory if not exists
if not os.path.isdir(Config.DOWNLOAD_LOCATION):
    os.makedirs(Config.DOWNLOAD_LOCATION)

# Temporary dictionary
user_files = {}

@bot.on_message(filters.text & filters.private)
async def handle_url_message(client, message: Message):
    url = message.text.strip()
    file_name = "SampleVideo.mp4"
    file_size = "373.24 MB"
    user_id = message.from_user.id

    user_files[user_id] = {
        "url": url,
        "file_name": file_name
    }

    buttons = [
        [InlineKeyboardButton("📄 Default", callback_data="default_upload"),
         InlineKeyboardButton("✏️ Rename", callback_data="rename_file")]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)

    await message.reply_text(
        f"📥 **How would you like to upload this link?**\n\n"
        f"**Name:** `{file_name}`\n**Size:** `{file_size}`",
        reply_markup=reply_markup
    )

@bot.on_callback_query(filters.regex("default_upload"))
async def upload_default(client, callback_query):
    user_id = callback_query.from_user.id
    file_info = user_files.get(user_id)

    if file_info:
        await callback_query.message.edit_text(f"Uploading `{file_info['file_name']}` with default name...")
    else:
        await callback_query.message.edit_text("No file info found.")

@bot.on_callback_query(filters.regex("rename_file"))
async def ask_rename(client, callback_query):
    await callback_query.message.edit_text("✏️ Please send the new file name (with extension like `.mp4`)")

    @bot.on_message(filters.text & filters.private & filters.user(callback_query.from_user.id))
    async def get_new_name(client, msg):
        new_name = msg.text.strip()
        user_id = msg.from_user.id
        file_info = user_files.get(user_id)

        if file_info:
            file_info["file_name"] = new_name
            await msg.reply_text(f"Uploading file as `{new_name}`...")
        else:
            await msg.reply_text("File info not found.")

print("🎊 Bot is starting... 🎊")
bot.run()
