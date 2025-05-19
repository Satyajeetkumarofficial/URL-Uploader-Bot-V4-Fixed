# ©️ LISA-KOREA | @LISA_FAN_LK | NT_BOT_CHANNEL | @NT_BOTS_SUPPORT | LISA-KOREA/UPLOADER-BOT-V4

# [⚠️ Do not change this repo link ⚠️] :- https://github.com/LISA-KOREA/UPLOADER-BOT-V4

import os
from plugins.config import Config
from pyrogram import Client

app = Client("my_bot", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN)

if __name__ == "__main__":
    app.run()

    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)
    plugins = dict(root="plugins")
    Client = Client("@UploaderXNTBot",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    sleep_threshold=300,
    plugins=plugins)
    print("🎊 I AM ALIVE 🎊  • Support @NT_BOTS_SUPPORT")
    Client.run()


# === Rename Feature Start ===

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram import filters

# Dictionary to temporarily store user file info
user_files = {}

@app.on_message(filters.text & filters.private)
async def handle_url_message(client, message: Message):
    url = message.text.strip()

    # Simulate extracting file name and size
    file_name = "SampleVideo.mp4"
    file_size = "373.24 MB"
    user_id = message.from_user.id

    # Save file details temporarily
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

@app.on_callback_query(filters.regex("default_upload"))
async def upload_default(client, callback_query):
    user_id = callback_query.from_user.id
    file_info = user_files.get(user_id)

    if file_info:
        await callback_query.message.edit_text(f"Uploading `{file_info['file_name']}` with default name...")
        # Upload logic here
    else:
        await callback_query.message.edit_text("No file info found.")

@app.on_callback_query(filters.regex("rename_file"))
async def ask_rename(client, callback_query):
    await callback_query.message.edit_text("✏️ Please send the new file name (with extension like `.mp4`)")

    @app.on_message(filters.text & filters.private & filters.user(callback_query.from_user.id))
    async def get_new_name(client, msg):
        new_name = msg.text.strip()
        user_id = msg.from_user.id
        file_info = user_files.get(user_id)

        if file_info:
            file_info["file_name"] = new_name
            await msg.reply_text(f"Uploading file as `{new_name}`...")
            # Upload logic here
        else:
            await msg.reply_text("File info not found.")

# === Rename Feature End ===
