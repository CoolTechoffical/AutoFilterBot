import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Load environment variable for Fsub channel
FSUB_CHANNEL = os.getenv('FSUB_CHANNEL')  # Channel username (private or public)

# Function to check if the user has joined the FSUB channel
async def is_subscribed(client, user_id):
    try:
        member = await client.get_chat_member(FSUB_CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# Handler for sending the file
@Client.on_message(filters.private & filters.document)
async def send_file(client, message):
    user_id = message.from_user.id
    file_id = message.document.file_id  # Getting file_id from the document

    if await is_subscribed(client, user_id):
        # If the user is subscribed, send the file without a caption
        await message.reply_document(file_id)
    else:
        # If not subscribed, send the FSub request with a join button
        join_button = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("📢 Request to Join Channel 📢", url=f"https://t.me/{FSUB_CHANNEL}")],
                [InlineKeyboardButton("🔄 Try Again 🔄", callback_data=f"retry_{file_id}")]
            ]
        )
        await message.reply(
            "♦️ READ THIS INSTRUCTION ♦️\n\n"
            "🗣 If you want to get the file you're requesting, "
            "you must first join our channel by clicking the '📢 Request to Join Channel 📢' "
            "button or the link below. After joining, press the '🔄 Try Again 🔄' button "
            "to receive the file.\n\n"
            "👇 CLICK 'REQUEST TO JOIN CHANNEL' THEN CLICK 'TRY AGAIN' 👇",
            reply_markup=join_button
        )

# Handler for the "Try Again" button click
@Client.on_callback_query(filters.regex(r"retry_(.+)"))
async def check_subscription(client, callback_query):
    user_id = callback_query.from_user.id
    file_id = callback_query.data.split("_")[1]  # Extracting the file_id from callback data

    if await is_subscribed(client, user_id):
        # If the user is subscribed, send the file without a caption
        await callback_query.message.delete()  # Remove the previous message
        await client.send_document(callback_query.message.chat.id, file_id)
    else:
        # If the user still hasn't joined, prompt them again
        await callback_query.answer("You're not subscribed yet! Please join the channel first.", show_alert=True)
