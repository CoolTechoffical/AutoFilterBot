import os
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment variables
FSUB_URL = os.getenv("FSUB_URL")  # Join channel link

# Handle /start command
@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client, message: Message):
    user_id = message.from_user.id

    # Send the "Join Channel" and "Try Again" buttons if the user is not verified
    btn = [
        [InlineKeyboardButton("Join Channel", url=FSUB_URL)]
    ]
    
    # Check if the start command contains a file reference
    if len(message.command) > 1 and message.command[1] != "subscribe":
        try:
            kk, file_id = message.command[1].split("_", 1)
            pre = 'checksubp' if kk == 'filep' else 'checksub'
            btn.append([InlineKeyboardButton("🔄 Try Again", callback_data=f"{pre}#{file_id}")])
        except (IndexError, ValueError):
            btn.append([InlineKeyboardButton("🔄 Try Again", url=f"https://t.me/{client.username}?start={message.command[1]}")])
    
    await client.send_message(
        chat_id=message.from_user.id,
        text="Please Join My Updates Channel to use this Bot!",
        reply_markup=InlineKeyboardMarkup(btn),
        parse_mode=enums.ParseMode.MARKDOWN
    )

# Handle Try Again button via CallbackQuery
@Client.on_callback_query(filters.regex(r"^checksub#(.+)"))
async def check_subscription_callback(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    file_id = callback_query.data.split("#")[1]

    # Since we aren't checking subscription, we assume the user has joined
    # Delete the old message
    await callback_query.message.delete()

    # Send the file after they click Try Again
    await client.send_document(chat_id=user_id, document=file_id)
