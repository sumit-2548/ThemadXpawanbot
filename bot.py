from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

# Your bot token here
BOT_TOKEN = "8171331380:AAEOxdrZANqNYWxd84xwZ7N088FVvNBkCJ8"

# Class channel links
class_links = {
    "class9": "https://t.me/nexttoper9thAarambh",
    "class10": "https://t.me/nexttoper10thAarambh",
    "class11": "https://t.me/nexttoperclass11th"
}

# File mapping for each class image
class_images = {
    "class9": "class9.png",
    "class10": "class10th.png",
    "class11": "class11th.png"
}


# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("📘 Class 9", callback_data="class9"),
            InlineKeyboardButton("📗 Class 10", callback_data="class10"),
            InlineKeyboardButton("📙 Class 11", callback_data="class11")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send welcome image and message
    with open("thumbnail.png", "rb") as photo:
        message = await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo,
            caption="🎉 *Dear Student*,\n\nWelcome to *TheMadXpawan Bot*.\nChoose your class to start your Free Learning Journey 👇",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    # Save message ID to edit later
    context.user_data["welcome_message_id"] = message.message_id


# Class button click handler
async def class_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    class_selected = query.data
    link = class_links[class_selected]
    image_path = class_images[class_selected]

    caption = f"""✅ Thank you for using our bot!

🎯 This is your destination link: [Join now]({link})

🗂 Class: *{class_selected.capitalize()}*

🔥 _Is baar system faad denge!!_"""

    # Open the relevant image
    with open(image_path, "rb") as photo:
        # Edit the original welcome message with new photo and message
        await context.bot.edit_message_media(
            chat_id=query.message.chat_id,
            message_id=context.user_data["welcome_message_id"],
            media=InputFile(photo),
            reply_markup=None
        )

        # Edit caption separately
        await context.bot.edit_message_caption(
            chat_id=query.message.chat_id,
            message_id=context.user_data["welcome_message_id"],
            caption=caption,
            parse_mode="Markdown",
        )


# Main function to run the bot
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(class_button_handler))

    print("🤖 Bot is running...")
    await app.run_polling()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
