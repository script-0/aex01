#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from pymongo import MongoClient  # this lets us connect to MongoDB

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

APP_NAME = "https://aex01.herokuapp.com/"
PORT = int(os.environ.get("PORT", "8443"))
TOKEN = os.environ.get("BOT_SECRET")

mongoClient = MongoClient(
    "mongodb+srv://script0:script0@cluster0.0soh0.mongodb.net/aex01? retryWrites=true&w=majority"
)


def chatId(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text("The chat id is : " + str(update.message.chat.id))


def start(update, context):
    """Send a message when the command /start is issued."""
    # print(update)
    try:
        update.message.reply_text(
            "Hi " + update.message.chat.first_name + " !  Thank's"
        )
    except:
        update.message.reply_text(
            "Hi " + update.message.from_user.first_name + " !  Thank's"
        )

    mongoClient.aex01.messages.insert_one(update.to_dict())


def notCommandAllowed(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("Not commands Allowed")


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("Just a simple Bot. Not commands found")


def echo(update, context):
    """Echo the user message."""
    mongoClient.aex01.messages.insert_one(update.to_dict())
    pass


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("chatId", notCommandAllowed))
    dp.add_handler(CommandHandler("start", notCommandAllowed))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.update, echo))

    # log all errors
    dp.add_error_handler(error)
    updater.start_webhook(
        listen="0.0.0.0", port=PORT, url_path=TOKEN, webhook_url=APP_NAME + TOKEN
    )
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
