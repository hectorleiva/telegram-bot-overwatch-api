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

# Format prestige rating as stars after their current level
def prestigeFormatting(prestigeLevel, currentLevel):
    prestigeSign = str(currentLevel)
    if prestigeLevel > 0:
        for i in range(prestigeLevel):
            prestigeSign += " *"
        return prestigeSign
    else:
        return prestigeSign

def overwatch(bot, update, args):
    if determineWhiteListedUsers(update.message.chat_id) is False:
        bot.send_message(chat_id=update.message.chat_id,
                text="I'm sorry, you are not white-listed for this service")
        return

    bot.send_message(chat_id=update.message.chat_id,
            text="Ok, looking up the information, one moment...")

    for battletag in args:
        """
        The API can only take in '-' as the delimiter instead of the pound-sign
        that is often used 
        """
        battletagParsed = battletag.replace('#', '-')
        requestUrl = "{0}/api/v3/u/{1}/stats".format(overwatchAPIDomain, battletagParsed)
        userAgent = "{0}/0.1".format(bot.name)
        headers = { 'user-agent': userAgent }

        logger.info('requestUrl: %s', requestUrl)

        r = requests.get(requestUrl, headers=headers)

        logger.info('the response: %s', r)
        logger.info('status code: %s', r.status_code)
        logger.info('text: %s', r.text)

        if r.status_code == 200:
            logger.info('response was good')
            response = r.json()
            quickPlayGameStats = response['us']['stats']['quickplay']['game_stats']
            quickPlayOverallStats = response['us']['stats']['quickplay']['overall_stats']
            logger.info('quickPlayOverallStats: %s', quickPlayOverallStats)

            currentLevel = prestigeFormatting(quickPlayOverallStats['prestige'], quickPlayOverallStats['level'])

            battletagStats = "Current Quickplay overall stats for {battletag}\n"
            battletagStats += "Level: {currentLevel}\n"
            battletagStats += "Number of Wins: {numOfWins}\n"
            battletagStats += "Competitive Rank: {compRank}\n"
            battletagStats += "Total Hours Played: {totalHours}"
            bot.send_message(chat_id=update.message.chat_id,
                text=battletagStats.format(
                    battletag=battletag,
                    currentLevel=currentLevel,
                    numOfWins=quickPlayOverallStats['wins'],
                    compRank=quickPlayOverallStats['comprank'],
                    totalHours=quickPlayGameStats['time_played']))
        else:
            bot.send_message(chat_id=update.message.chat_id,
                    text='Hmmm, something is wrong with the API request. Sorry! I am unable to return back stats')

def main():
    updater = Updater(sys.argv[1])
    dispatch = updater.dispatcher
    dispatch.add_handler(CommandHandler('start', start))
    dispatch.add_handler(CommandHandler('info', start))
    dispatch.add_handler(CommandHandler('overwatch', overwatch, pass_args=True))

    # Begin the polling process
    updater.start_polling()

    # Ensure that we can stop threads with Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
