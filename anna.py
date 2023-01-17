import os,sys
import json 
import discord
import time
import requests
import random
from discord.ext import tasks
import asyncio
import csv

from requests.api import head

client = discord.Client()

try:
    with open("C:\\Users\\k41st\\Desktop\\Anna\\schedule.txt", 'r') as reader:
        # Read & print the entire file
        linesList = reader.readlines()
        reader.close() 
    
    counter = linesList[-2]
    scheduleList = linesList[-1]
    scheduleList = scheduleList.replace("'",'"')            
   
    scheduleList = json.loads(scheduleList)
    monthList = scheduleList.get('month')
    dayList = scheduleList.get('day')
    hourList = scheduleList.get('hour')
    minuteList = scheduleList.get('minute')
    taskList = scheduleList.get('task')
    userList = scheduleList.get('user')
    print("Scheduling Loaded")
    workingshed = True
except:
    print("Scheduling Failed to load")
    workingshed = False




#setups.txt
with open("C:\\Users\\k41st\\Desktop\\Anna\\setups.txt", 'r') as reader2:
    linesList2 = reader2.readlines()
    reader2.close() 

adminList = json.loads(linesList2[0].replace('\'',"\""))
serverRequest = json.loads(linesList2[1].replace('\'',"\""))
people = json.loads(linesList2[2].replace('\'',"\""))
print('Setup Loaded')







#default reponses
sandwichResponses = ["Cum sandwich coming right up", "I'll give you a knuckle sandwich", "true!", "What toppings do you want", "shit sandwich time", "Dinner time honey, oh wait no one loves you"]
loveResponse = ["Maybe look in the mirror", "Take a shower", "Improve yourself","Dont be an ugly bastard next time","Be nice","Ill be your gf", "You're asking a bot about this? Thats depressing"]
yesNoResponses = ["Yes","Perhaps" , "No" , "Yes", "Yes" , "Yes" , "No"]

#usable prefixes other then anna
prefixList = ["slave, "]

stream = os.popen('curl  -H "Authorization:Bearer B23H6T7BVEE33NPFXWG2DQEEVTCFC3UN" "https://api.wit.ai/message?v=20201026&q=whats%20the%20weather"')
output = stream.read()
res = json.loads(output) 
x = res.get("intents")
intentDict = x[0]
print(intentDict.get("name"))
print("Natural Language Loaded")

user = client.get_user(258716099971907597)


def monthConvert(month):
    if month == "Jan":
        num = 1
    elif month == "Feb":
        num = 2
    elif month == "Mar":
        num = 3
    elif month == "Apr":
        num = 4
    elif month == " May":
        num = 5
    elif month == "Jun":
        num = 6
    elif month == "Jul":
        num = 7
    elif month == "Aug":
        num = 8
    elif month == "Sep":
        num = 9
    elif month == "Oct":
        num = 10
    elif month == "Nov":
        num = 11
    elif month == "Dec":
        num = 12
    else:
        num = 0
    return(num)

def getDay():
    current = str(time.asctime())
    day = current[0:3]
    if day == "Tue":
        day = "Tuesday"
    elif day == "Wed":
        day = "Wednesday"
    elif day == "Thu":
        day = "Thursday"
    elif day == "Sat":
        day = "Saturday"
    else:
        day = day + "day"

    day += " " + current[8:10]
    return(day)

def getTime():
    
    ampm = "AM"
    current = str(time.asctime())
    hours = int(current[11:13])
    minutes = current[14:16]
    if hours > 12:
        ampm = "PM"
        hours -= 12
    
    return(hours,minutes,ampm)



    


ball = True




@tasks.loop(minutes=1,reconnect = True)
async def checktime():



    global ball
    global minuteList
    global hourList
    global taskList
    global userList
    global monthList
    global dayList
    global counter
   
    current = str(time.asctime())
    day = current[8:10]
    hours = current[11:13]
    minutes = current[14:16]
    month = current[4:7]
    month = str(monthConvert(month))

    if hours == "12" and ball == False:
        kike = client.channel_get(758525210252541952)
        await kike.send("Ball? @everyone")
        ball = True
    elif hours == "13":
        #ball = False
        pass
    if workingshed and minutes in minuteList:
        index = minuteList.index(minutes)
        checkH,checkD,checkM = hourList[index],dayList[index],monthList[index]
        
  
        
        if checkH == hours and checkD == day and checkM == month:

            task = taskList[index]
            ScheduledUser = userList[index]
        
            monthList.pop(index)
            minuteList.pop(index)
            dayList.pop(index)
            hourList.pop(index)
            taskList.pop(index)
            userList.pop(index)
            
            ScheduledUser = int( ScheduledUser)

            SU = await client.fetch_user(int(ScheduledUser))

            ReminderMes = SU.mention + " Reminder: " + task

            await SU.send(ReminderMes)
    
  

            Newcounter = counter.replace("\n", "")
            counter = int(Newcounter)
            counter +=1
            
            newList = f"\n{scheduleList}"
            counter = f"\n{counter}"

            with open("C:\\Users\\k41st\\Desktop\\Anna\\schedule.txt", 'r+') as reader:
                reader.readlines()
                reader.write(counter)
                reader.write(newList) 
                reader.close()

@client.event
async def on_connect():
    print("Connecting...")



@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    
    me = await client.fetch_user(258716099971907597)
    
    await client.change_presence(activity = discord.Game("Anna, "))
    whatday = 'Good morning it is '+ str(getDay()) + ''
    hours,minutes,ampm = getTime()
    whattime = f"It's {hours}:{minutes} {ampm}"
    
    


    print("Waking up... ")
    print(whatday)
    print(whattime)



            


    try:
        await me.send("Waking up... ")        
        await me.send(whatday)
        await me.send(whattime)
    except AttributeError:
        print("Still not working")
    checktime.start()
    

if False:
    class textMessage():
        def __init__(self,author,content):
            self.author = author
            self.content = content

    async def testingoffline():

                
        testmes = textMessage(258716099971907597,"Anna, test")

        await on_message(testmes)

    



@client.event
async def on_message(message):


    global minuteList
    global hourList
    global taskList
    global userList
    global monthList
    global dayList
    global counter
    global scheduleList
                                                                                                                 

    
    commanded = 0

    if message.author == client.user:
        return

    if message.content == "Anna, shutdown" and message.author.id in adminList:
        await message.channel.send("Goodnight")
        quit()

    if message.content == "Anna, restart" and message.author.id in adminList:
        os.execl(sys.executable, sys.executable, *sys.argv)

    if message.content == "Admin test":
        ScheduledUser = 258716099971907597

        SU = await client.fetch_user(int(ScheduledUser))
 
        await SU.send("Worked")

    if message.content == "Anna, come here":
        await message.channel.send("What do you need")
        serverRequest.append(message.author.id)
        return  
    
    if message.content == "Anna, leave now":
        await message.channel.send("Bye then")
        serverRequest.remove(message.author.id)
        return

    if message.content == "Annatest":
        datajson = json.loads(requests.get("https://newsapi.org/v2/top-headlines?country=ca&apiKey=e6a4038112ef4f86be1045e9b735d67d").text)
        if datajson.get("status") == "ok":
            articles = datajson.get("articles")
        else:
            message.channel.send("News services down sorry please try again later")
        headlines = ""
        for x in range(10):
            headline = str(articles[x].get("source").get("name")) + ": " + str(articles[x].get("title"))
            headlines = headlines + headline + "\n"
        await message.channel.send(headlines)
    

    if message.content== "Anna":             
        

        user = client.get_user(258716099971907597)
        
        await message.channel.send("I am awake")
        await message.author.create_dm()
        await message.author.send("Did you need my help?")
        await user.send("Called")
    
    #TODO
    if message.content.startswith("Settings add user"):
        personID = message.mentions[0].id
        nameIndex = message.content.find("?")
        name = message.content[nameIndex+1:]
        print(personID,name)
        response = "Stored: " + str(name) + " as " + str(personID)
        people[str(name)] = int(personID)
        await message.channel.send(response)
        with open("C:\\Users\\k41st\\Desktop\\Anna\\setups.txt", 'w') as settings:
            writeable = f"{adminList}" + "\n" + f"{serverRequest}" + "\n" + f"{people}"
            settings.write(writeable)

        

    for x in prefixList:
        if message.content.startswith(x):
            commanded = 1
        
    if message.content.startswith("Anna,") or message.content.startswith("anna, ")  or commanded == 1:
        
        if message.author.id in serverRequest:
            
            sendChannel = message.channel
        else:
            sendChannel = message.author
    
        commaLoc = message.content.find(',')
        query = message.content[commaLoc+1:]
        query = query.replace(" ", "%20")
        query = 'curl  -H "Authorization:Bearer B23H6T7BVEE33NPFXWG2DQEEVTCFC3UN" "https://api.wit.ai/message?v=20201026&q="' + query 
        print(query)
        stream = os.popen(query)
        output = stream.read()
        res = json.loads(output) 
        x = res.get("intents")
        try:
            intentsDict = x[0]
            intent =intentsDict.get("name")
            confidence = intentsDict.get("confidence")
            print(intent, confidence)
        except IndexError:
            await sendChannel.send("I cant help with that")
            print("Intent unkown")
            return
        
        
        
        
        
        
        
        if confidence < 0.9:
            await sendChannel.send("I'm not sure what you asked, but keep trying and I'll learn")
        
        
        elif intent == "Weather" :
            torontoWeather = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Toronto&units=metric&appid=77c70f1c51e96bd537ad56546e6a5970')
            weather = torontoWeather.text
            weather = json.loads(weather)
            CurrentWeather = weather["weather"]
            temp = weather["main"]
            CurrentWeather = CurrentWeather[0]
            mainWeather = CurrentWeather["main"]
            CurrentTemp = round(temp["temp"])
            HighTemp = round(temp["temp_max"])
            LowTemp = round(temp["temp_min"])
            Humidity = round(temp["humidity"])
            TempMes = f"Currently the weather is {CurrentTemp}° "
            TempMes2 = f"There is a high of {HighTemp}° and a low of {LowTemp}° for today"
            TempMes3 = f"The humidity is {Humidity}%"
            await sendChannel.send(TempMes)
            await sendChannel.send(TempMes2)
            await sendChannel.send(TempMes3)
            
            if mainWeather == "Rain":
                weatherMes = "It is currently raining"
            elif mainWeather == "Clouds":
                weatherMes = "It is currently cloudy"
            else:
                weatherMes = "It is currently sunny"
            await sendChannel.send(weatherMes)
        
        
        
        
        elif intent == "Scheduling":
        
            reciverID = message.author.id
        
        
        
            with open("C:\\Users\\k41st\\Desktop\\Anna\\schedule.txt", 'r') as reader:
                # Read & print the entire file
                linesList = reader.readlines()
                reader.close()
            
            counter = linesList[-2]
            scheduleList = linesList[-1]
            
            scheduleList = scheduleList.replace("'",'"')
            scheduleList = json.loads(scheduleList)
            
            
            ents = res.get("entities")
            datetime = ents.get("wit$datetime:datetime")
            
            try:
                datetime = datetime[0]
                time = datetime.get("value")
                confidcneTime = datetime.get("confidence")
            except TypeError:
                await sendChannel.send("You need to schedule a time")
                return
            
            month = time[5:7]
            day = time[8:10]
            hour = time[11:13]
            minute = time[14:16]
            
            taskGet = ents.get("wit$message_body:scheduling_task")
            try:
                taskDict = taskGet[0]
                task = taskDict.get("body")
            except:
                try:
                    bodyGet = ents.get("wit$message_body:message_body")
                    bodyDict = bodyGet[0]
                    task = bodyDict.get("body")
                except TypeError:
                    await sendChannel.send("Im sorry can you repeat or reword that")
                    return
                
          
            
            monthList = scheduleList.get('month')
            dayList = scheduleList.get('day')
            hourList = scheduleList.get('hour')
            minuteList = scheduleList.get('minute')
            taskList = scheduleList.get('task')
            userList = scheduleList.get('user')
            
            
            monthList.append(month)
            dayList.append(day)
            hourList.append(hour)
            minuteList.append(minute)
            taskList.append(task)
            userList.append(reciverID)
               
            
            
            counter = counter.replace("\n", "")
            counter = int(counter)
            counter +=1
            
            newList = f"\n{scheduleList}"
            counter = f"\n{counter}"

            with open("C:\\Users\\k41st\\Desktop\\Anna\\schedule.txt", 'w') as reader:
                
                reader.write(counter)
                reader.write(newList) 
                reader.close()
            
            
            
            await sendChannel.send("Reminder noted")
            
            
        elif intent == "Messaging":
            senderID = message.author.id
            if senderID not in adminList:
                response = ("You are not a validated user")
                await sendChannel.send(response)
            else:
                ents = res.get("entities")
                personGet = ents.get('person:person')[0].get('body')
                messageEnt = ents.get('wit$message_body:message_body')[0].get('body')
                personID = people[personGet]
                person = await client.fetch_user(personID)
                await person.send(messageEnt)
                response = "Message sent to " + str(person.name) + "#" + str(person.discriminator)
                await sendChannel.send(response)

            
        
        elif intent == "Yes_No":
            
            response = random.choice(yesNoResponses)
            await sendChannel.send(response)
        
        
            
            
        elif intent == "Sandwich":
            
            response = random.choice(sandwichResponses)
            await sendChannel.send(response)
            

            
            
        elif intent == "Love_Life":
            
            response = random.choice(loveResponse)
            await sendChannel.send(response)
            
            
        elif intent == "News":
            datajson = json.loads(requests.get("https://newsapi.org/v2/top-headlines?country=ca&apiKey=e6a4038112ef4f86be1045e9b735d67d").text)
            if datajson.get("status") == "ok":
                articles = datajson.get("articles")
            else:
                message.channel.send("News services down sorry please try again later")
            headlines = ""
            for x in range(10):
                headline = str(articles[x].get("source").get("name")) + ": " + str(articles[x].get("title"))
                headlines = headlines + headline + "\n"
            await message.channel.send(headlines)
            print(datajson)
                

        elif intent == "Blacklist":
            
            ents = res.get("entities")
            query = ents.get("querytype:querytype")[0].get("body").lower()
            person = ents.get("person:person")[0].get("body").capitalize()
            fullName = False
            if ' ' in person:
                firstName = person.split()[0]
                lastName = person.split()[1]
                fullName = True
            else:
                firstName = person

            with open('C:\\Users\\k41st\\Desktop\\Anna\\Blacklist\\blacklist.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                        if row['first name'] == firstName:
                            answer = row[query]

            await message.channel.send(answer)

          
        else:
            await sendChannel.send("I can't help with that")


        

        
        
        

client.run("NzcwMzE2MjgyMzk0MDUwNjEx.X5by8Q.DmpbS-huAsdk2XXpWzXzSBQDzJc")

