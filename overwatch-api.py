#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Ask your bot for your latest Overwatch stats against SunDwarf's
# Overwatch API.
from telegram.ext import Updater, CommandHandler, Job
from whitelisting import *

import sys
import requests
import logging

overwatchAPIDomain = 'https://owapi.net'

# 0) The script itself
# 1) The Token
# 2) The whitelisted id for testing
cmdargs = str(sys.argv)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(bot, update):
    msg = "Hey there {user_name}! I'm {bot_name}, \n"
    msg += "My current functionality is to return Overwatch info based on the username you've given me\n"
    msg += "/overwatch + [username] - Will return their latest stats\n"
    msg += "Warning, only whitelisted users can actually do requests!"

    bot.send_message(chat_id=update.message.chat_id,
            text=msg.format(
                user_name=update.message.from_user.first_name,
                bot_name=bot.name))

def overwatch(bot, update, args):
    r = requests.get('{overwatchAPIDomain}')

    if r.stats_code == 200:
        bot.send_message(chat_id=update.message.chat_id,
            text="I should be returning you something")

def main():
    updater = Updater(sys.argv[1])
    dispatch = updater.dispatcher
    dispatch.add_handler(CommandHandler('start', start))
    dispatch.add_handler(CommandHandler('info', start))
    # dispatch.add_handler(CommandHandler('overwatch', overwatch))

    # Begin the polling process
    updater.start_polling()

    # Ensure that we can stop threads with Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
