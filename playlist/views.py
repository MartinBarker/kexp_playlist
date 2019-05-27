from django.shortcuts import render
from django.http import HttpResponse
#from .models import Album
from django.shortcuts import render, redirect
from django.http import Http404
from django.template import loader

import json #for converting / parsing json
import requests #for making get request on kexp api
import urllib.request
#import datetime #for getting dateTime
from datetime import datetime, timedelta
from django.utils import timezone

from .models import plays

globalPlayData = {}

def index(request):
    global globalPlayData

    #get last 1 hour of play data as json 
    begin_time, end_time, playData = getPlayData(1)

    #update database to only include plays with comments, or made within the timeframe, 
    updateDatabase(begin_time, end_time, playData)

    #create new play objects
    test_play = plays()
    test_play.playID = '56826'
    test_play.playtypeID = 1
    test_play.playtypeName = 'audio song'
    test_play.airdate =  '2019-05-26T01:16:56Z'
    test_play.artistName = 'the cars'
    test_play.releaseName = 'albumname 2'
    test_play.releaseImage = 'www.image.jpg'
    test_play.releaseYear = '1987'
    test_play.trackName = 'new song title'
    test_play.comment = 'my cool comment'
    #add plays row to database
    #test_play.save()

    #sort database by airdate
    plays.objects.extra(order_by=['airdate']) 


    #get plays table data from database
    playsData = plays.objects.all().order_by('-airdate')

    #store as global variable
    globalPlayData = playData

    numSongs = len(playData['results'])

    #get all comments from database
    #all_comments = Comments.objects.all()
    all_comments = 0

    
    #django automatically looks for templates folder in app directory
    context = { 
        'plays': playsData,
        'numPlays': len(playsData),
        'all_comments': all_comments,
        'begin_time': begin_time,
        'end_time': end_time
    }

    #redner html and context
    return render(request, 'playlist/index.html', context)    

#get play data from last 'timeFrame' number of hours
def getPlayData(timeFrame):

    #get end_time and start_time

    end_time_raw = datetime.now(timezone.utc)
    end_time_pacific = end_time_raw - timedelta(hours=7)
    end_time = end_time_raw.isoformat() #gets formatted as 2019-05-25T23:36:32.667638+00:00
    #print("end_time_raw = ")
    #print(end_time_raw)
    end_time = str(end_time)[:-6]  #remove las 7 chars (+00:00) offset
    #print("end_time = ", end_time )
    

    #get start_time = 1 hour before end_time
    begin_time_raw = end_time_raw - timedelta(hours = timeFrame)
    begin_time_pacific = end_time_pacific - timedelta(hours = timeFrame)
    #print("begin_time_raw = ", str(begin_time_raw))
    begin_time = begin_time_raw.isoformat()
    begin_time = str(begin_time)[:-6]
    #print("begin_time = ", begin_time)

    #format initial api request url 
    targetURL = "https://legacy-api.kexp.org/play/?format=json&begin_time=" + begin_time + "&end_time=" + end_time + "&ordering=-airdate" #&limit=40" #usually 20, 21 songs played in an hour. set limit to 30 for now

    print("targetURL = ")
    print(targetURL)

    #save json data from url
    jsonData = requests.get(targetURL).json()
 
    #hardcoded url
    #targetURL = "https://legacy-api.kexp.org/play/?format=json&start_time=2019-05-24T23:00:00&ordering=-airdate"
    #hardcoded example data: raw python string (dont interpret any escapes)
    #json_string = r'''{ "next": "https://legacy-api.kexp.org/play/?format=json&limit=3&offset=3", "previous": null, "results": [ { "playid": 2661588, "playtype": { "playtypeid": 1, "name": "Media play" }, "airdate": "2019-05-25T01:49:00Z", "epoch_airdate": 1558748940000, "epoch_airdate_v2": "/Date(1558748940000)/", "archive_urls": { "64": "http://50.234.71.239:8090/stream-64.mp3?date=2019-05-25T01:49:00Z", "32": "http://50.234.71.239:8090/stream-32.mp3?date=2019-05-25T01:49:00Z", "256": "http://50.234.71.239:8090/stream-256.mp3?date=2019-05-25T01:49:00Z", "128": "http://50.234.71.239:8090/stream-128.mp3?date=2019-05-25T01:49:00Z" }, "artist": { "artistid": 23485, "name": "Ida Corr", "islocal": false }, "release": null, "releaseevent": null, "track": { "trackid": 1374873, "name": "Let Me Think About It" }, "label": null, "comments": [ { "commentid": 1228353, "text": "Playing all women+ artists and bands with women tonight. Songs about empowerment and women's rights.This artist from Denmark." } ], "showid": 103814 }, { "playid": 2661587, "playtype": { "playtypeid": 1, "name": "Media play" }, "airdate": "2019-05-25T01:44:00Z", "epoch_airdate": 1558748640000, "epoch_airdate_v2": "/Date(1558748640000)/", "archive_urls": { "64": "http://50.234.71.239:8090/stream-64.mp3?date=2019-05-25T01:44:00Z", "32": "http://50.234.71.239:8090/stream-32.mp3?date=2019-05-25T01:44:00Z", "256": "http://50.234.71.239:8090/stream-256.mp3?date=2019-05-25T01:44:00Z", "128": "http://50.234.71.239:8090/stream-128.mp3?date=2019-05-25T01:44:00Z" }, "artist": { "artistid": 143629, "name": "Cesaria Evora", "islocal": false }, "release": { "releaseid": 352103, "name": "Cabo Verde", "largeimageuri": null, "smallimageuri": null }, "releaseevent": { "releaseeventid": 702075, "year": 1997 }, "track": { "trackid": 1374872, "name": "Sangue Di Belrona (Dave Spritz remix)" }, "label": { "labelid": 38550, "name": "Nonesuch Records" }, "comments": [ { "commentid": 1228352, "text": "Legendary vocalist from Cape Verde! https://www.cesaria-evora.com/" } ], "showid": 103814 }, { "playid": 2661586, "playtype": { "playtypeid": 1, "name": "Media play" }, "airdate": "2019-05-25T01:40:00Z", "epoch_airdate": 1558748400000, "epoch_airdate_v2": "/Date(1558748400000)/", "archive_urls": { "64": "http://50.234.71.239:8090/stream-64.mp3?date=2019-05-25T01:40:00Z", "32": "http://50.234.71.239:8090/stream-32.mp3?date=2019-05-25T01:40:00Z", "256": "http://50.234.71.239:8090/stream-256.mp3?date=2019-05-25T01:40:00Z", "128": "http://50.234.71.239:8090/stream-128.mp3?date=2019-05-25T01:40:00Z" }, "artist": { "artistid": 184207, "name": "Amber Mark", "islocal": false }, "release": { "releaseid": 328454, "name": "Conexão", "largeimageuri": null, "smallimageuri": null }, "releaseevent": { "releaseeventid": 702073, "year": 2018 }, "track": { "trackid": 1374870, "name": "Love Me Right" }, "label": { "labelid": 74477, "name": "Virgin EMI Records" }, "comments": [ { "commentid": 1228351, "text": "Check out her exclusive Guest DJ mix when she visited KEXP to host Midnight in a Perfect World. https://www.kexp.org/read/2017/10/12/midnight-in-a-perfect-world-amber-mark/?t=1555111381691" } ], "showid": 103814 } ] }'''
    #json_data = json.loads(json_string)
    #numberOfSongs = len(json_data["results"][0])
    #print(numberOfSongs)
    
    #return jsonData
    return begin_time_pacific, end_time_pacific, jsonData

def comment(request, playid):
    #add comment
    commentText = request.POST['commentInput']
    #print("commentText = ", commentText)
    instance = plays.objects.get(id=playid)
    instance.comment = commentText
    instance.save()
    #redirect to /playlist/page
    return redirect('/playlist/') 
    
def delete(request, playid):
    #grab play by playid in database
    instance = plays.objects.get(id=playid)
    #delete it
    instance.delete()
    #redirect to /playlist/page
    return redirect('/playlist/')

def updateDatabase(begin_time, end_time, playData):
    #begin_time = one hour ago
    #begin_time_pacific = begin_time - timedelta(hours=7)
    print("begin_time = ", str(begin_time))
    


    #dt, _, us = begin_time.partition(".")
    #dt = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
    #begin_time_pacific = dt - timedelta(hours=7)
    #end_time_pacific = dt - timedelta(hours=6)
    #print("begin_time_pacific = ")
    #print(begin_time_pacific)

    #end_time = current time
    #begin_time_pacific = end_time - timedelta(hours=7)
    #playData = json data of last 60 mins pulled from API
    
    

    #remove any songs not within the timeframe from the database [if song outside timeframe has comment, keep it]
    #iterate through every value in database
    #if targetPlay has no comment:
        #if targetPlay.airdate is before (<) begin_time: 
            #delete targetPlay from database

    print("iterating thorugh db")
    items = plays.objects.all()
    for item in items.values('id', 'airdate', 'comment'):
        print("is item['airdate'] = ", item['airdate'], " < ", begin_time)
        if item['airdate'] < begin_time:
            print("yes. item[id] = ", item['id'])
            play = plays.objects.get(id = item['id'])
            play.delete()

    for song in playData['results']:
        print("checking if play_to_insert is unique")
        playid_to_insert = song['playid']
        instances = plays.objects.filter(playID = playid_to_insert)
        if(len(instances) == 0):
            play_to_insert = getPlayFromJSON(song)
            play_to_insert.save()


def getPlayFromJSON(song):
    #convert json 'song' to database 'play' object
    play_to_insert = plays()
    play_to_insert.playID = song['playid']
    play_to_insert.playtypeID = song['playtype']['playtypeid']
    play_to_insert.playtypeName = song['playtype']['name']
    
    #play_to_insert.airdate = song['airdate']

    kexp_airdate_string = song['airdate']
    #print("kexp_airdate_string = ", kexp_airdate_string)
    #remove last character "Z"
    kexp_airdate_string = kexp_airdate_string[:-1]
    #convert string to dateTime object
    dt, _, us = kexp_airdate_string.partition(".")
    dt = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
    #convert to pacific
    pacific_conversion = dt - timedelta(hours=7)
    #print("pacific_conversion = ")
    #print(pacific_conversion)
    #store new time
    play_to_insert.airdate = pacific_conversion


    play_to_insert.artistName = insert_if_field_1_exists(song, 'artist', 'name')
    play_to_insert.releaseName = insert_if_field_1_exists(song, 'release', 'name')
    play_to_insert.releaseImage = insert_if_field_1_exists(song, 'release', 'largeimageuri')
    play_to_insert.releaseYear = insert_if_field_1_exists(song, 'releaseevent', 'year')
    play_to_insert.trackName = insert_if_field_1_exists(song, 'track', 'name')
    play_to_insert.comment = ''
    return play_to_insert

def insert_if_field_1_exists(jsonData, field1, field2):
    #if field1 is not null, return field2 inside field1
    if jsonData[field1] != None:
        return jsonData[field1][field2]
    else:
        #field1 is null, so return null 
        return None