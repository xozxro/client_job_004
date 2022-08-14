# bot.py
import os
#from turtle import color
import discord
from dotenv import load_dotenv
#from backports import configparser
import time
from discord.ext import commands
from discord.utils import get
# LOAD CONFIG FILE
import data

import traceback
import requests
import os

# SET VARIABLE FROM CONFIG FILE
token = 'MTAwODM2OTE3ODgzMjUzNTY0Mg.GyJJvu.0TFi1PM8imOnNdvtwZ_eubqGvC__QO2V52hyCg'
channel_id = ''

# START DISCORD CLIENT
client = discord.Client()

class Tracker:
    
    def __init__(self):
        self.pendingResponses = {}
        self.emojiAdd = {}
            
    def add(self,id,msgID):
        self.pendingResponses[msgID] = id
        self.emojiAdd[msgID] = 0
        
    def addResponse(self,id,response):
        
        # get request id from message id
        if str(id) in self.pendingResponses.keys():
            id = self.pendingResponses[str(id)]
        
        # use to send appropriate request    
        if 'yes' in response.lower():
            res = requests.get('http://localhost:5000/app/postDiscordResponse/'+str(id)+'/'+'yes',)
            return res.text

        if 'no' in response.lower():
            res = requests.get('http://localhost:5000/app/postDiscordResponse/'+str(id)+'/'+'no',)
            return res.text
    
    def countEmojiAdd(self,mesasgeId):
        
        if str(messageId) in self.emojiAdd.keys():
            emoji



################### ENDPOINTS

# BOT START MSG
@client.event
async def on_ready():
    
    print(f'[*] bot connected.')

# NEW TICKET MESSAGE
@client.event
async def on_message(message):
    
    if len(message.embeds) > 0 and str(message.channel.id) == str(data.channelID):
        
        messageEmbed = message.embeds[0]
        
        if len(messageEmbed.fields) > 0:
            
            names = [x.name for x in messageEmbed.fields]
            
            if 'Location:' in names and 'Ticket info:' in names and 'Total Cost' in names:
                
                # confirmed that it's a ticker info embed in right channel. 
                # add to list of pending confirmations
                id = messageEmbed.description.split('|')[-1].replace('ID','').strip()
                msgID = str(message.id)
                tracker.add(id,msgID)
                
                # now lets add the bottons so on an action with them, we can retrieve
                # the ticket info id from the reacted to message id, then make
                # an api call to set the response for the ticket info id approp
                
                await message.add_reaction('🟢')
                await message.add_reaction('🔴')
    
            pass

# TICKET MESSAGE RECIEVED APPROVE / DENYU
@client.event       
async def on_raw_reaction_add(payload):
    
    if (payload.emoji.name == '🟢' or payload.emoji.name == '🔴') and str(payload.member) != 'Ticket Bot#0933' and str(payload.user_id) != '1008369178832535642':
        
        if payload.emoji.name == '🟢': successBool = tracker.addResponse(payload.message_id,'yes')
        if payload.emoji.name == '🔴': successBool = tracker.addResponse(payload.message_id,'no')
        
        print(successBool)
        
        if successBool == 'Success':
            tracker.pendingResponses.pop(str(payload.message_id))
        
        
        
tracker = Tracker()
client.run(token)
