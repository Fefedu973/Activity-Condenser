import discord
from discord.ext import commands
import json
from pypresence import Presence
import time
import nest_asyncio
import os

nest_asyncio.apply()

src = os.path.join(os.getenv("APPDATA"),"Activity-Condenser")
settingssrc = os.path.join(src,"settings.json")
datasrc = os.path.join(src,"data.json")
errors = os.path.join(src,"errors.json")

with open(settingssrc) as f:
    settings = json.load(f)
    print(settings)


TOKEN = settings['Bot_Token']
BOT_PREFIX = '!'



intents = discord.Intents().all()
temp = {}
ls_dict = {"Presence":[]}


bot = commands.Bot(command_prefix=BOT_PREFIX, intents = intents)

try :
    client_id = settings['Client_ID']
    RPC = Presence(client_id )
    RPC.connect()
except Exception as e:
    print('______________________________________')
    print(e)
    errorfinal = {"Errors":e}
    jsonString = json.dumps(errorfinal, indent=4, default=str)
    jsonFile = open(errors, "w")
    jsonFile.write(jsonString)
    print('______________________________________')
    exit()

async def rpc():
        print(RPC.update(state="...", details="Loading"))
        time.sleep(5)
        RPC.close()

@bot.event
async def on_ready():
    print('Logged in as :')
    print(bot.user.name)
    print('ID :')
    print(bot.user.id)
    print('\n')
    await rpc()
    


@bot.event
async def on_presence_update(before, after):
    afterdebug = str(after)
    if afterdebug == settings['username'] :
        print('New Activity detected')
        print('User :', after)
        print('___')
        print(before, after)
        global ls_dict
        for i, a in enumerate(after.activities):
            if type(a) == discord.activity.Activity:
                print("\n")
                print("Activity n°", i, "Name :")
                print(after.activities[i].name)
                temp = {'ID': i, 'AppID': after.activities[i].application_id, 'Name': after.activities[i].name, 'URL': after.activities[i].url, 'Details': after.activities[i].details, 'State': after.activities[i].state, 'Timestamps': after.activities[i].timestamps, 'large_image': after.activities[i].large_image_url, 'large_text': after.activities[i].large_image_text, 'small_image': after.activities[i].small_image_url, 'small_text': after.activities[i].small_image_text, 'Buttons': after.activities[i].buttons, 'End': after.activities[i].end, 'Party': after.activities[i].party, 'Start': after.activities[i].start}
                ls_dict["Presence"].append(temp)
                print('Updated', after.activities[i].name)
                print('___')
        jsonString = json.dumps(ls_dict, indent=4, default=str)
        jsonFile = open(datasrc, "w")
        jsonFile.write(jsonString)
        print('Json File Updated')
        temp = {}
        ls_dict = {"Presence":[]}
    else :
        print('The user is not the one you want to track, maybe you entered the wrong username in the settings page ?')

try :
    bot.run(TOKEN)
except Exception as e:
    print('______________________________________')
    print(e)
    errorfinal = {"Errors":e}
    jsonString = json.dumps(errorfinal, indent=4, default=str)
    jsonFile = open(errors, "w")
    jsonFile.write(jsonString)
    print('______________________________________')
    exit()
