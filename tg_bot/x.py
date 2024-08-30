#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

import logging
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Импорт функции из основного файла
from answer_generation.rag import process_query

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize the retriever outside of any handlers to ensure it's created only once
# retriever = create_vectorstore()

# Define a few command handlers. These usually take the two arguments update and context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def handle_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the user query and process it with the LLM."""
    query = update.message.text

    # Обработка запроса с использованием основной логики
    response = process_query(query)

    # Отправка ответа обратно пользователю
    await update.message.reply_text(response)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6909103286:AAFus5QDZ5XxF96jcKTvKSU5GEMECLHhMbE").read_timeout(60).write_timeout(60).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - handle the query
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_query))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
