#####################################################################################
# simple API built to handle subscriptions and alerts for the Nyria.io trading bot. |
# written by ZXRO 2021 // xozxro.io nyria.io flytlabs.dev                           |
#####################################################################################



# INIT
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

class Log:

    def __init__(self):
        self.twitterCount = 0
        self.discordCount = 0

    def twitterCount(self):
        self.twitterCount += 1
        return str(self.twitterCount)

    def discordCount(self):
        print('yes')
        self.discordCount += 1
        return str(self.discordCount)
    


# APP START
##########

###### FLASK FUNCTIONS
##################################################################

# route for passing new ticket data

# REQUEST EXAMPLE
# 127.0.0.1/postNewData?username=user_5&title=xyz&date=12/12/23&location=austin_tx_-_xyz_stadium&ticketInfo=2_tickers_sec_xyz_row_5_seats


app = Flask(__name__)

class appView(FlaskView):
    
    default_methods = ['GET','POST']

    def __init__(self):
        
        self.default_methods = ['GET','POST']
        self.sentData = []
    
    # EXTENSION POSTS DATA
    @route('/postNewData/', methods=['POST'])
    def postNewData(self) -> str:
        
        if request.method == 'POST': 
            
            content = request.json
            id = random.randint(100000,900000)
            self.pendingDiscordResponses[id] = content
            print(content)
            
            self.title = '['+content['eventName']+']('+str(content['checkoutURL'])+')'
            print(self.title)
            self.webhook = DiscordWebhook(url='https://discord.com/api/webhooks/1001115041971585067/WvgMnD5e0gTReHZOE5mlAkJcOgSMdl4NW59iqKvi9FRv55fMPVucm6-eTliu-YkB5tKa', username='', content='')
            self.embed = DiscordEmbed(title=content['eventName'], description=' > ' + content['eventDate'] + '  |  [*Ticket Link*](https://checkout.ticketmaster.com/35b0f95635c34818af6053d61c5cfd6d?ccp_src=2&ccp_channel=0&edp=https%3A%2F%2Fwww.ticketmaster.com%2Fmotley-cruedef-leppardpoisonjoan-jett-and-the-indianapolis-indiana-08-16-2022%2Fevent%2F05005C4FDA473AD6%3F_ga%3D2.144253937.558213141.1656781326-527735984.1656781326&f_appview=false&f_appview_ln=false&f_appview_version=1&f_layout=)', color='00FFE4')
        
            self.embed.add_embed_field(name='Location:', value='\n'+content['eventLocation']+'\n')
            self.embed.add_embed_field(name='Ticket info:', value='\n'+content['ticketDetails']+'\n')
            self.embed.add_embed_field(name='Total Cost', value='\n**'+str(content['totalCost'])+'**\n')
            self.embed.set_image(url=content['minimapImageUrl'])
            self.embed.set_author(name=content['name_of_user'])
            self.webhook.add_embed(self.embed)
            self.response = self.webhook.execute()
            print(self.response)
            
            return str(id)
    
    # DISCORD BOT GETS DATA
    @route('/getNewData/', methods=['GET'])
    def getNewData(self):
        
        replyData = {}
        for key,value in self.pendingDiscordResponses.items():
            if key not in self.sentData:
                replyData[key] = value
                self.sentData.append(key)
            else:
                pass
        
        return replyData
                
    # DISCORD BOT SENDS ADMIN RESPONSE
    @route('/postDiscordResponse/<id>/<string:yesNo>')
    def postDiscordResponse(self,id,yesNo):
        try:
            if int(id) in self.pendingDiscordResponses.keys():
                self.pendingDiscordResponses[int(id)] = yesNo.lower()
                return 'Success'
            else:
                print(self.pendingDiscordResponses)
                print(id)
                return 'Invalid ID'
        except:
            return 'False'
        
    # EXTENSION GETS ADMIN RESPONSE
    @route('/getDiscordResponse/<id>')
    def getDiscordResponse(self,id):
        
        if int(id) in self.pendingDiscordResponses.keys():
            if self.pendingDiscordResponses[int(id)] == 'yes' or self.pendingDiscordResponses[int(id)] == 'no':
                return self.pendingDiscordResponses[int(id)]
            else:
                
                print(self.pendingDiscordResponses)
                return 'False'
        else:
            print(self.pendingDiscordResponses)
            print(id)
            return 'Invalid ID'        
        

    

    '''# route for passing twitter tags
    @route('/postUserData/Twitter/<twitterTag>/')
    def botGetNewData(twitterTag):

        try:

            twitterTag = twitterTag.replace('_', '#')

            # open the discord csv file
            with open(r'twitters.csv', "a", newline='') as myfile:
                wr = csv.writer(myfile)
                wr.writerow([twitterTag.strip()])

            myfile.close()

            print('[!] added twitter user ' + twitterTag)
            print('[*] ' + counter.twitterCount() + ' new users added in current uptime')

            return 'True'

        except:

            return 'False'


    # route for bot to pass alerts
    # validates source of alert and passes it to the notifcation functions.
    # these functions read the data collected in the CSVs and distribute the alert appropriately
    @route('/postAlert/<alertData>')
    def botPushResp(alertData):

        # retrieve request IP for validation.
        requestIPAddress = request.remote_addr

        print('[!] ALERT request coming from IP ' + str(requestIPAddress))

        try:

            if validateRequest(alertData,requestIPAddress):
                validRequestLog(alertData)

                # format alertData
                tradearray = alertData.split('-')

                # push alerts
                pushDiscordNotif(tradearray)
                pushTwitterNotif(tradearray)
                pushTelegramNotif(tradearray)

                return 'True'

            else:

                invalidRequestLog(requestIPAddress)

                return 'Invalid Request'

        except:

            return 'False'

    # route for bot to pass alerts
    # validates source of alert and passes it to the notifcation functions.
    # these functions read the data collected in the CSVs and distribute the alert appropriately
    @route('/postAlert/<alertData>')
    def extGetBotResp(alertData):

        # retrieve request IP for validation.
        requestIPAddress = request.remote_addr

        print('[!] ALERT request coming from IP ' + str(requestIPAddress))

        try:

            if validateRequest(alertData,requestIPAddress):
                validRequestLog(alertData)

                # format alertData
                tradearray = alertData.split('-')

                # push alerts
                pushDiscordNotif(tradearray)
                pushTwitterNotif(tradearray)
                pushTelegramNotif(tradearray)

                return 'True'

            else:

                invalidRequestLog(requestIPAddress)

                return 'Invalid Request'

        except:

            return 'False'''
            
appView.register(app)
appView.pendingDiscordResponses = {}

if __name__ == '__main__':

    print('[!] starting app')

    os.chdir(os.getcwd())
    
    print('[!] working in dir ' + str(os.getcwd()))

    log = Log()

    print('[!] data log created')
    
    app.run()
        
    print('[!] bot started.')

    





###### INTERNAL FUNCTIONS
##################################################################

# validation, alerts

def formatData(request):
    
    loadRequest = json.loads(request)


def pushDiscordNotif(tradearray):
    pass

def pushTwitterNotif(tradearray,watching=False):

    consumer_key = "tfPVqNFjFRaweJ5IQSFi6PoHl"
    consumer_secret = "S1KBrLw7ajVVuTUzqUZSJni4G0WyfSwiyYL9evucVFOWm5qWYc"
    access_token = "1394713976521494532-PjkPmNZ0FhNmoGYGWjcFeoRidG3byh"
    access_token_secret = "1Y2V74VAI6dCxELAh9mhp8woIi9nr3BTAXFOwp9go3m9c"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # set ticker variable
    ticker = '$SPY'

    # check for long or sell

    now = datetime.now()
    minute = now.strftime("%M")
    hour = now.strftime("%H")

    if watching:

        tweet = '[' + str(hour) + ':' + str(minute) + ']' + ' Watching ' + ticker + ' for a trade.'
        first_tweet = api.update_status(tweet)

        return

    if type == 'long':
        # create tweet
        tweet = '[' + str(hour) + ':' + str(minute) + ']' + ' Long ' + ticker + ' @ ' + str(
            round(float(tradearray[3]), 2))
        # + '\nTrade win rate: ' + tradearray[-1]

        # tradearray = [current_time, dataDict['high'], dataDict['low'], dataDict['close'], dataDict['RSI'], dataDict['VWAP'], dataDict['ema12'], dataDict['ema26'], dataDict['MACD'], dataDict['STOCH']]

        # tweet the tweet
        first_tweet = api.update_status(tweet)

        return



def pushTelegramNotif(tradearray):

    now = datetime.now()
    minute = now.strftime("%M")
    hour = now.strftime("%H")

    try:

        message = '[' + str(hour) + ':' + str(minute) + ']' + ' Long ' + tradearray[-2] + ' @ ' + str(
            round(float(tradearray[3]), 2))

        telegram_send.send(messages=[message])
        return True
    except:
        return False

# log messages, error handling

def validRequestLog(alertData):
    print('[*] request is VALID.')
    print('[*] alert      -----> ' + alertData)

def invalidRequestLog(requestIPAddress):
    print('[*] request is INVALID.')
    print('[*] logging requesting IP to log.')
    print('[!] IP                     -----> ' + str(requestIPAddress))
