import discord
import datetime

import foodflex.util.data as data
import foodflex.util.config as config
import foodflex.periods.voting as voting
import foodflex.periods.submissions as submissions

from foodflex.util.bot import bot
from foodflex.util.logging import logger


@bot.event
async def on_message(message):
    # don't respond to our own messages
    if message.author.bot:
        return

    # ignore messages in any channel but the main one
    if message.channel != bot.get_channel(config.main_channel_id):
        return

    now = datetime.datetime.now()
    hour = int(now.strftime('%H'))
    minute = int(now.strftime('%M'))

    await bot.process_commands(message)

    if data.period == 'submissions' and len(message.attachments) > 0:
        logger.info(f'Submission from \'{message.author.display_name}\' ({str(message.author.id)})')
        await submissions.process_submission(message)

    elif data.period == 'voting' and len(message.clean_content) == 1:
        logger.info(f'Vote \'{message.clean_content}\' from \'{message.author.display_name}\' ({str(message.author.id)})')
        await voting.check_vote(message)
