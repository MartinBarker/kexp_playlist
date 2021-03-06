from django.shortcuts import render, redirect
from datetime import datetime, timedelta #for calculating / converting datetime
from django.utils import timezone
import json #for converting / parsing json
import requests #for making get request to kexp api url

from .models import plays #import plays database object from playlist/models.py

#when called, update database and return last hour of songs played
def index(request):

    #begin_time = dateTime object of current time - 1 hour
    #end_time = dateTime object of current time
    #playData = json object of last hour of play data from KEXP api
    begin_time, end_time, json_playData = getPlayData(1) #gave int parameter for better testing (see tests.py)
    #example: begin_time = 7pm, end_time = 8pm

    #update database to only include unique plays made within the timeframe, 
    updateDatabase(begin_time, end_time, json_playData)

    #get plays table data from database ordered by dateTime airdate
    db_playsData = plays.objects.all().order_by('-airdate')

    #create context of usefull variables to pass into the html view
    context = { 
        'plays': db_playsData,        #database values sorted by airdate          
        'numPlays': len(db_playsData),   #number of songs in database
        'begin_time': begin_time,     #dateTime object begin_time =  current time - 1 hour
        'end_time': end_time          #dateTime object end_time = current_time
    }

    #return rendered index.html with context
    return render(request, 'playlist/index.html', context)    

#get play data from kexp api for last 'timeFrame' number of hours
def getPlayData(timeFrame):

    #end_time_raw = end_time as dateTime object 
    end_time_raw = datetime.now(timezone.utc)
    #end_time = end_time_raw formatted for kexp api url request
    end_time = end_time_raw.isoformat()         
    #gets formatted as 2019-05-25T23:36:32.667638+00:00
    end_time = str(end_time)[:-5]  
    #remove las 6 chars (+00:00) offset

    #begin_time_raw = dateTime object 1 hour before end_time
    begin_time_raw = end_time_raw - timedelta(hours = timeFrame)
    #begin_time = begin_time_raw formatted for kexp api url request
    begin_time = begin_time_raw.isoformat()
    begin_time = str(begin_time)[:-6]

    #format initial api request url 
    targetURL = "https://legacy-api.kexp.org/play/?format=json&begin_time=" + begin_time + "&end_time=" + end_time + "&ordering=-airdate" 

    #print for debugging purposes
    #print("targetURL = ")
    #print(targetURL)

    #make request to targetURL and save as json data
    jsonData = requests.get(targetURL).json()
    
    #convert end_time_raw and begin_time_raw (UTC) to pacific time for easier displaying 
    end_time_pacific = end_time_raw - timedelta(hours=7)
    begin_time_pacific = end_time_pacific - timedelta(hours = timeFrame)

    #return begin and end time (pacific) and jsonData from get request to kexp api url
    return begin_time_pacific, end_time_pacific, jsonData

#add comment to database
def comment(request, playid):
    #get comment text from request
    commentText = request.POST['commentInput']
    #get instance from database where primaryKey id = playid
    instance = plays.objects.get(id=playid)
    #save commentText to instance
    instance.comment = commentText
    #save instance to database
    instance.save()
    #redirect to /playlist/
    return redirect('/playlist/') 

#delete play from database
def delete(request, playid):
    #grab play by playid in database
    instance = plays.objects.get(id=playid)
    #delete it
    instance.delete()
    #redirect to /playlist/page
    return redirect('/playlist/')

#update database to only include songs from playData during the timeframe
def updateDatabase(begin_time, end_time, playData):
    #begin_time = dateTime object of current time - 1 hour
    #end_time = dateTime object of current time
    #playData = json data pulled from kexp API

    # 1. Clean up the database by removing any songs not within the timeframe from the database

    #delete rows from database where airdate comes before begin_time
    results = plays.objects.filter(airdate__lt=begin_time)
    results.delete()

    # 2. Insert new plays from the playData into the database
    #need to ensure only unique plays are inserted into database because whenever the user refreshes /playlist/ it updates the view to display the last 60 minutes of plays, so if the user refreshes the page multiple times in the span of one hour there will be overlap of songs received from the kexp api url request.

    #iterate through every play from playData json 
    for song in playData['results']:
        #get playid of play we want to insert
        playid_to_insert = song['playid']
        #get number of instances from database with same playid
        instances = plays.objects.filter(playID = playid_to_insert)
        #if there are no instances of a database row with this playid:
        if(len(instances) == 0):
            #convert json play into object we can add to database
            play_to_insert = getPlayFromJSON(song)
            #save play_to_insert to database
            play_to_insert.save()

#convert json 'song' to database 'play' object
def getPlayFromJSON(song):
    #create new blank play to insert
    play_to_insert = plays()
    
    #set fields:

    #these fields will always be present: (no matter if its an airbreak, song, etc)
    play_to_insert.playID = song['playid']
    play_to_insert.playtypeID = song['playtype']['playtypeid']
    play_to_insert.playtypeName = song['playtype']['name']

    #get airdate string from json song and format it into a dateTime object
    kexp_airdate_string = song['airdate']                # 2019-06-04T05:50:00Z
    
    #remove last character "Z"
    kexp_airdate_string = kexp_airdate_string[:-1]       # 2019-06-04T05:50:00

    #convert string to dateTime object
    dt = datetime.strptime(kexp_airdate_string, "%Y-%m-%dT%H:%M:%S")

    #convert to pacific time (for easier displaying)
    pacific_conversion = dt - timedelta(hours=7)

    #store new pacific dateTime object
    play_to_insert.airdate = pacific_conversion

    #these fields may be 'None' depending if its an airdate / song, so use function to only insert second value if first value is not 'None'
    play_to_insert.artistName = insert_if_field_1_exists(song, 'artist', 'name')
    play_to_insert.releaseName = insert_if_field_1_exists(song, 'release', 'name')
    play_to_insert.releaseImage = insert_if_field_1_exists(song, 'release', 'largeimageuri')
    play_to_insert.releaseYear = insert_if_field_1_exists(song, 'releaseevent', 'year')
    play_to_insert.trackName = insert_if_field_1_exists(song, 'track', 'name')
    #set comment by default to empty (could have set it to dj comment, but the comment for this assignment is different)
    play_to_insert.comment = ''
    
    #return our play object
    return play_to_insert

#check json data to see if field1 is 'None'
def insert_if_field_1_exists(jsonData, field1, field2):
    #if field1 is not null, return field2 inside field1
    if jsonData[field1] != None:
        return jsonData[field1][field2]
    else:
        #if field1 is null, return null 
        return None