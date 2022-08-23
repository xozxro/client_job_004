# IMPORTS
##########
import datetime

from flask import Flask, request, jsonify
from flask_restful import Resource,Api
from flask_classful import FlaskView, route
import csv
import os
import json
import random
from discord_webhook import DiscordWebhook, DiscordEmbed


###### FLASK FUNCTIONS
##################################################################

app = Flask(__name__)

class appView(FlaskView):
    
    default_methods = ['GET','POST']

    def __init__(self):
        
        self.default_methods = ['GET','POST']
        self.sentData = []
    
    # EXTENSION POSTS DATA
    @route('/postNewData', methods=['POST'])
    def postNewData(self) -> str:
        print(True)
        
        if request.method == 'POST': 
            
            # get content
            try:
                content = json.load(request, strict=False)
            except:
                content = request.json
            
            # generate id
            id = random.randint(100000,900000)
            while id in self.pendingDiscordResponses.keys():
                id = random.randint(100000,900000)
            self.pendingDiscordResponses[id] = content
            
            # push content to server
            self.title = '['+content['eventName']+']('+str(content['checkoutURL'])+')'
            self.webhook = DiscordWebhook(url='https://discord.com/api/webhooks/1008416489738616853/uTJZe1coksy76_CUbCybLYNy7PtKYLJ-oBgKA5oQXHKB-OzZ6mNe9JYpDpaMq5vdwM4D', username='', content='')
            self.embed = DiscordEmbed(title=content['eventName'], description=' > ' + content['eventDate'] + '  |  [*Ticket Link*](https://checkout.ticketmaster.com/35b0f95635c34818af6053d61c5cfd6d?ccp_src=2&ccp_channel=0&edp=https%3A%2F%2Fwww.ticketmaster.com%2Fmotley-cruedef-leppardpoisonjoan-jett-and-the-indianapolis-indiana-08-16-2022%2Fevent%2F05005C4FDA473AD6%3F_ga%3D2.144253937.558213141.1656781326-527735984.1656781326&f_appview=false&f_appview_ln=false&f_appview_version=1&f_layout=) | ID ' + str(id), color='00FFE4')
            self.embed.add_embed_field(name='Location:', value='\n'+content['eventLocation']+'\n')
            self.embed.add_embed_field(name='Ticket info:', value='\n'+content['ticketDetails']+'\n')
            self.embed.add_embed_field(name='Total Cost', value='\n**'+str(content['totalCost'])+'**\n')
            self.embed.set_image(url=content['minimapImageUrl'])
            self.embed.set_author(name=content['name_of_user'])
            self.webhook.add_embed(self.embed)
            self.response = self.webhook.execute()
            
            # success?
            print(self.response)
            
            # return ID to extension for response retrieval
            return str(id)
    
    # DISCORD BOT SENDS ADMIN RESPONSE
    @route('/postDiscordResponse/<id>/<string:yesNo>')
    def postDiscordResponse(self,id,yesNo):
        
        try:
            
            if int(id) in self.pendingDiscordResponses.keys():
                self.pendingDiscordResponses[int(id)] = yesNo.lower()
                # response recieved and saved into existing ID successfully.
                return 'Success'
            else:
                # id doesn't exist
                return 'Invalid ID'
            
        except:
            # error
            return 'False'
        
    # EXTENSION GETS ADMIN RESPONSE
    @route('/getDiscordResponse/<id>')
    def getDiscordResponse(self,id):
        
        if int(id) in self.pendingDiscordResponses.keys():
            
            if self.pendingDiscordResponses[int(id)] == 'yes' or self.pendingDiscordResponses[int(id)] == 'no':
                # repsonse found. return the value and remove from the pending
                # response list as we recieved one and no longer need the data.
                returnVal = self.pendingDiscordResponses[int(id)]
                self.pendingDiscordResponses.pop(int(id))
                return returnVal
            else:
                # no response yet
                return 'False'
            
        else:
            # id doesn't exist
            return 'Invalid ID'        
        
      
appView.register(app)
appView.pendingDiscordResponses = {}


if __name__ == '__main__':

    print('[!] starting app')

    os.chdir(os.getcwd())
    
    print('[!] working in dir ' + str(os.getcwd()))
    
    print('[!] bot started.')
    
    app.run()