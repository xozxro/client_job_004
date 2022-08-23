import os
import time

import discord
from discord.utils import get
from discord.ext import commands
#from discord_buttons_plugin import *
from discord import Button, ButtonStyle
import data

import traceback
import requests
import os

# SET VARIABLE FROM CONFIG FILE
token = 'MTAwODM2OTE3ODgzMjUzNTY0Mg.GLUMMS.8rLYCuzYbzjrUiG7bke5HQ12R7ZGHbNNZ8-A4M'
channel_id = ''

# START DISCORD CLIENT
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
#buttons = ButtonsClient(client)

class Tracker:
    
    def __init__(self):
        
        self.pendingConfirmation = {}
        self.pendingResponses = {}
        self.emojiAdd = {}
            
    def addPendingConfirmation(self,message,id,msgid):
        self.pendingConfirmation[id] = (message,msgid)
        
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
@bot.event
async def on_ready():
    
    print(f'[*] bot connected.')
    

class Menu(discord.ui.View):
    

    @discord.ui.button(label="Yes", custom_id="yes", style=discord.ButtonStyle.green)
    async def button_yes(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass
    
    @discord.ui.button(label="No", custom_id="no", style=discord.ButtonStyle.red)
    async def button_no(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass

# NEW TICKET MESSAGE
@bot.event
async def on_message(message):
        
    print(message)
    
    if len(message.embeds) > 0 and str(message.channel.id) == str(data.channelID):
        
        messageEmbed = message.embeds[0]
        
        if len(messageEmbed.fields) > 0:
            
            names = [x.name for x in messageEmbed.fields]
            
            if 'Location:' in names and 'Ticket info:' in names and 'Total Cost' in names:
                
                # confirmed that it's a ticker info embed in right channel. 
                # add to list of pending confirmations
                id = messageEmbed.description.split('|')[-1].replace('ID','').strip()
                
                # create new emebed
                newEmbed = discord.Embed(title=messageEmbed.title, description=messageEmbed.description)
                
                # copy fields to new embed
                for setField in messageEmbed.fields:
                    newEmbed.add_field(name=setField.name, value=setField.value, inline=False)
                
                # add to confirmable embed list
                tracker.addPendingConfirmation(newEmbed,str(id),str(message.id))
                                            
                # now lets add the bottons so on an action with them, we can retrieve
                # the ticket info id from the reacted to message id, then make
                # an api call to set the response for the ticket info id approp
                
                #await message.add_reaction('🟢')
                #await message.add_reaction('🔴')
    
            pass
        
    test = await bot.process_commands(message)
    print(test)
        
        
@bot.command(name='yes')
async def yes(ctx, id):
    if id == 'all':
        for key,value in tracker.pendingConfirmation.items():
            try:
                await ctx.channel.send(embed=value[0], view=Menu())
                delMsg = await ctx.channel.fetch_message(value[1])
                await delMsg.delete()
            except Exception as exception:
                traceback.print_exc()
    else:
        try:
            await ctx.channel.send(embed=tracker.pendingConfirmation[id][0], view=Menu())
            delMsg = await ctx.channel.fetch_message(tracker.pendingConfirmation[id][1])
            await delMsg.delete()
        except Exception as exception:
            traceback.print_exc()


# TICKET MESSAGE RECIEVED APPROVE / DENYU
@bot.event       
async def on_raw_reaction_add(payload):
    
    if (payload.emoji.name == '🟢' or payload.emoji.name == '🔴') and str(payload.member) != 'Ticket Bot#0933' and str(payload.user_id) != '1008369178832535642':
        
        if payload.emoji.name == '🟢': successBool = tracker.addResponse(payload.message_id,'yes')
        if payload.emoji.name == '🔴': successBool = tracker.addResponse(payload.message_id,'no')
        
        print(successBool)
        
        if successBool == 'Success':
            tracker.pendingResponses.pop(str(payload.message_id))
        
    await bot.process_commands(message)

        
tracker = Tracker()
bot.run(token)
