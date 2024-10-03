import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Get the channel URL from the environment variable
FSUB_URL = os.getenv("FSUB_URL", "https://t.me/your_channel")  # Set your default channel URL here

@Client.on_message(filters.command(["start"]))
async def start(client, message):
    user_id = message.from_user.id
    
    # Check if the user is a member of the channel
    try:
        member = await client.get_chat_member(FSUB_URL, user_id)
        if member.status in ["member", "administrator", "creator"]:
            # If the user is already a member, proceed with sending the requested file
            await message.reply("You are already a member! I'll send you the movie now.")
            # Here you can send the requested file using its file_id
            # Example: await message.reply_document(file_id='FILE_ID')
        else:
            raise Exception("User is not a member")
    
    except:
        # If the user is not a member, send the FSUB request with buttons
        join_button = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("📢 Request to Join Channel 📢", url=FSUB_URL)],
                [InlineKeyboardButton("🔄 Try Again 🔄", callback_data="try_again")]
            ]
        )

        fsub_message = (
            "♦️ READ THIS INSTRUCTION ♦️\n\n"
            "🗣 If you want to get the movie you requested, you must request to join our channel first by "
            "clicking the '📢 Request to Join Channel 📢' button or the link below. After joining, click the "
            "'🔄 Try Again 🔄' button to receive the movie.\n\n"
            "👇 CLICK 'REQUEST TO JOIN CHANNEL' THEN CLICK 'TRY AGAIN' 👇"
        )
        
        await message.reply(fsub_message, reply_markup=join_button)

# Callback query handler for the "🔄 Try Again 🔄" button
@Client.on_callback_query(filters.regex("try_again"))
async def try_again(client, callback_query):
    user_id = callback_query.from_user.id
    
    # Check if the user is a member of the channel
    try:
        member = await client.get_chat_member(FSUB_CHANNEL, user_id)
        if member.status in ["member", "administrator", "creator"]:
            await callback_query.message.edit("Thank you for joining! I'll send you the movie now.")
            # Here you can send the requested file using its file_id
            # Example: await callback_query.message.reply_document(file_id='FILE_ID')
        else:
            raise Exception("User is not a member")
    
    except:
        await callback_query.answer("You haven't joined the channel yet. Please join and try again.", show_alert=True)
