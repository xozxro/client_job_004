# bot.py
import os
#from turtle import color
import discord
from dotenv import load_dotenv
#from backports import configparser
import time
import data
from discord.ext import commands
from discord.utils import get
# LOAD CONFIG FILE
import traceback
import requests
import os

# SET VARIABLE FROM CONFIG FILE
token = data.botToken
emoji = data.cross_post_emoji
channel_id = data.cross_post_channel_id
allowed_ids = data.cross_post_allowed_users

# START DISCORD CLIENT
client = discord.Client()


#### ENDPOINTS
# BOT READ MESSAGE
@client.event
async def on_ready():
    print(f'[*] bot connected.')


# MESSAGE REACTED TO WITHIN SELECTED CHANNEL
@client.event
async def on_message(message):
    if len(message.embeds) > 0:
        messageEmbed = message.embeds[0]
        if len(messageEmbed.fields) > 0:
            # do stuff here, find ID, add reactions, then add path to watch for message reactions on messages with an id in saved dictionary.
            # upon reaction, send api request to api server, then delete from dict so reactions don't trigger anything.
    
        
    
client.run(token)
