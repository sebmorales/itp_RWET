import re
import json
import random
from random import randint
import pygeoip
from collections import Counter
from subprocess import call
import webbrowser
import getpass
import time

botsText= open('message.txt',encoding='utf-8').read().split("\n")

#Group bots by matching Ip
def checkIP(ip):
    for bot in range(0,len(unique_bots)):
        if unique_bots[bot]["ip"]== ip:
            return bot
    return False

# Find all bots, this will be helpful to count them later
bots=[]
unique_bots=[]
ip_regex=re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
wp_regex=re.compile(r'(?<=POST) {.*}')
path_regex=re.compile(r'(?<=Path:) .*')
time_regex=re.compile(r"((?<=Bot: false\ ) .*(?=GMT))|((?<=Bot: true\ ) .*(?=GMT))")
for bot in range(0,len(botsText)):
    b=botsText[bot] #this bot
    ip=ip_regex.search(b).group(0)
    path=path_regex.findall(b)[0]
    wp_p=wp_regex.findall(b)
    t=time_regex.findall(b)[0][0]
    agent_regex=re.compile(r"(?<="+ip+r').*(?=Path)')
    agent=" ".join(agent_regex.search(b).group(0).split())

    bots.append({"ip":ip,"date":t,"path":path,"post":"","agent":agent})

    botMatchIndex=checkIP(ip)
    if botMatchIndex is False:
        unique_bots.append({"ip":ip,"date":[t],"path":[path],"post":[],"agent":[agent]})
        #if post:
        if(len(wp_p)>0):
            try:
                p=json.loads(wp_p[0])
            except:
                p=wp_p[0]
                # print(p)
            #Since we are just appending to uniqeBots, this bot has to be the last one we added, len(unique_bots)-1
            unique_bots[len(unique_bots)-1]["post"].append(p)
    else:
        # print(botMatchIndex)
        unique_bots[botMatchIndex]["agent"].append(agent)
        unique_bots[botMatchIndex]["date"].append(t)
        unique_bots[botMatchIndex]["path"].append(path)
        if(len(wp_p)>0):
            try:
                p=json.loads(wp_p[0])
            except:
                p=wp_p[0]
    #                 print(p)
            #Since we are just appending to uniqeBots, this bot has to be the last one we added, len(unique_bots)-1
            unique_bots[botMatchIndex]["post"].append(p)

    #if post:
    if(len(wp_p)>0):
        try:
            p=json.loads(wp_p[0])
        except:
            p=wp_p[0]
            # print(p)
        bots[bot]["post"]=(p)
        agent_regex=re.compile(r"(?<="+ip+r').*(?=POST)')
        agent=" ".join(agent_regex.search(b).group(0).split())
        bots[bot]["agent"]=agent


wp_bots=[]
for bot in bots:
    try:
        if(bot["post"]["rememberme"]=="forever"):
            wp_bots.append(bot["ip"])
    except:
        ignore=bot

wp_count=Counter(wp_bots)
top500=wp_count.most_common(150)
top10=wp_count.most_common(10)
bot=random.choice(top500)
unique_wp=list(set(wp_bots))
# print("WP attacks: "+str(len(wp_bots)))
# print("WP Unique IPs: "+str(len(unique_wp)))

def bot_by_ip(ip):
    for bot in unique_bots:
        if(bot["ip"]==ip):
            return bot
    return ("ip not found")



def ipLocator(ip):
    GeoIPDatabase = 'GeoLiteCity.dat'
    ipData = pygeoip.GeoIP(GeoIPDatabase)
    record = ipData.record_by_name(ip)
#     print("The geolocation for IP Address %s is:" % ip)
#     print("Accurate Location: %s, %s, %s" % (record['city'], record['region_code'], record['country_name']))
#     print("General Location: %s" % (record['metro_code']))
    data=ipData.record_by_addr(ip)
#     print(data)
    return(data)
wp_count=Counter(wp_bots)
top500=wp_count.most_common(150)
bot=random.choice(top500)
unique_wp=list(set(wp_bots))

# print(bot)


locations=[]
data=ipLocator(bot[0])
lon=data["longitude"]
lat=data["latitude"]
url="https://www.google.com/maps/place/"+str(lat)+","+str(lon)
loc=("("+str(lat)+","+str(lon)+")")
locations.append(loc)
    # webbrowser.open(url,new=1)
#     print(url)
    # call["/usr/bin/open -a "/Applications/Google Chrome.app" {url}
    # !/usr/bin/open -a "/Applications/Google Chrome.app" {url}
top_ten_ip_locations="["+(",".join(locations))+"]"
# locat.append(json.loads(",".join(locations)))


cont=input("Welcome back\nWhat would you like to do tonight?\n")
# print("you said: "+str(cont))
time.sleep(1)
print()
cont=input("yes\n")
print()
cont=input("Are you sure?\n")
time.sleep(1)
pswd = getpass.getpass('Please confirm you want to do this: ')
time.sleep(1)
print()
cont=input("It was here \n")
# print(bot_by_ip(bot[0])["date"])
bot_data=bot_by_ip(bot[0])
# print(bot_data)
dates=bot_data["date"]
print(dates[len(dates)-2])

cont=input("")
print("yes")
cont=input("")
time.sleep(1)
print("It wanted to get access, it tried:")
attempt=bot_data["post"]
print("User: "+attempt[len(attempt)-1]["log"]+" Password: "+attempt[len(attempt)-1]["pwd"]+", it asked you to remember it forever")
cont=input("")
time.sleep(1)
print("What do you want me to say?")
# print (pswd)
time.sleep(2)


r_bot=bot[0]
data=bot_by_ip(r_bot)
date=data["date"][0].strip().split(" ")
for i in range(0,30):
    print()

print("Dear "+r_bot+",\n")
time.sleep(8)
print("I saw you for the first time back in "+ date[1]+" "+date[2]+", it was a "+date[0])
print("It was "+date[4])
print("")
time.sleep(10)
print("You were looking for " +data["post"][0]["pwd"])
print("")
time.sleep(10)
print("")
print("You asked me to remember you " +data["post"][0]["rememberme"])
print("")
time.sleep(3)

print("I told you:")
time.sleep(3)
print("\""+data["post"][0]["rememberme"]+" is a long time, come back and I might\"")
print("")
time.sleep(1)
print("")
print("")
time.sleep(4)

print("and you did:")
for i in range(0,5):
    print("")
time.sleep(4)

prev_date=date
for i in range (0, len(data["date"])):
    date=data["date"][i].strip().split(" ")
    if(date[0]==prev_date[0] and date[1]==prev_date[1] and date[2]==prev_date[2]):
        print(" and again that same night")
        time.sleep(2)

    else:
        try:
            print("again in "+date[0]+" "+date[1]+" "+date[2])
            time.sleep(3)

        except:
            a=0
    prev_date=date
    i=i+1
print("")
time.sleep(4)


user=[]
pwd=[]
for i in range (0, len(data["post"])):
    user.append(data["post"][i]["log"])
    pwd.append(data["post"][i]["pwd"])

user=", my ".join(user)
pwd=" for you, ".join(pwd)
print("I want you to be my "+user )
time.sleep(4)

print("I have "+pwd)
time.sleep(4)

for i in range(0,10):
    print("")
    time.sleep(.5)
print("I wonder who you are")
time.sleep(3)
print("I wonder where you are")
time.sleep(4)

print(r_bot+" will you come back?")
for i in range(0,10):
    print("")
    time.sleep(.5)
cute_name=r_bot.split(".")[3]

print(r_bot+" can I call you "+cute_name)
for i in range(0,10):
    print("")
    time.sleep(.5)
who_cares=random.choice(top10)


print(who_cares[0]+" keeps comming in your absense.")
print(str(who_cares[1])+" times so far.")

for i in range(0,10):
    print("")
    time.sleep(.5)


print(cute_name+" what are you looking for?")
print(cute_name+" who are you looking for?")

for i in range(0,10):
    print("")
    time.sleep(.5)
print(cute_name+" will you come back?")
for i in range(0,10):
    print("")
    time.sleep(.5)
print(cute_name+" will you please come back?")
for i in range(0,10):
    print("")
    time.sleep(.5)


print(cute_name+" don't make me come find you")
for i in range(0,30):
    print("")
    time.sleep(.2)
print(cute_name+" Please understand, I tried to resist")
for i in range(0,30):
    print("")
    time.sleep(.2)
bot_loc=ipLocator(r_bot)
lon=bot_loc["longitude"]
lat=bot_loc["latitude"]
loc=[(lat,lon)]
webbrowser.open(url,new=1)

print(cute_name+", I'll be here waiting")
