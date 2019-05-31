from django.test import TestCase
from .models import plays
from .views import getPlayData, comment

from django.utils import timezone
import datetime
from datetime import timedelta

from django.test.client import RequestFactory

from jsonschema import validate
import json



class PlaylistTestCase(TestCase):
    def setUp(self):
        #create instance with hard-coded values
        plays.objects.create(playID="12345", playtypeID="1", playtypeName="Media Play", artistName="Kraftwerk", releaseName="Computer World", releaseImage="https://www.images.com/2134.png", trackName="Pocket Calculator", comment="my comment", releaseYear="1976", airdate="2019-05-30 08:22:00-07")
        plays.objects.create(playID="12346", playtypeID="1", playtypeName="Media Play", artistName="Kraftwerk", releaseName="Computer World", releaseImage="https://www.images.com/2134.png", trackName="Pocket Calculator", comment="", releaseYear="1976", airdate="2019-05-30 08:22:00-07")

    def test_plays_database_model(self):
        #get instance from our database
        instance = plays.objects.get(playID="12345")

        #verify value stored correctly in db 
        self.assertEqual(instance.playID, "12345")
        self.assertEqual(instance.playtypeID, 1)
        self.assertNotEqual(instance.playtypeID, "1")
        self.assertEqual(instance.playtypeName, "Media Play")
        self.assertEqual(instance.artistName, "Kraftwerk")
        self.assertEqual(instance.releaseName, "Computer World")
        self.assertEqual(instance.releaseImage, "https://www.images.com/2134.png")
        self.assertEqual(instance.trackName, "Pocket Calculator")
        self.assertEqual(instance.comment, "my comment")
        self.assertEqual(instance.releaseYear, "1976")
        self.assertEqual(instance.airdate, datetime.datetime(2019, 5, 30, 15, 22, tzinfo=datetime.timezone.utc))

        #verify type of each variable in database
        self.assertEqual(True, isinstance(instance.playID, str))
        self.assertEqual(True, isinstance(instance.playtypeID, int))
        self.assertEqual(True, isinstance(instance.playtypeName, str))
        self.assertEqual(True, isinstance(instance.artistName, str))
        self.assertEqual(True, isinstance(instance.releaseName, str))
        self.assertEqual(True, isinstance(instance.releaseImage, str))
        self.assertEqual(True, isinstance(instance.trackName, str))
        self.assertEqual(True, isinstance(instance.comment, str))
        self.assertEqual(True, isinstance(instance.releaseYear, str))
        self.assertEqual(True, isinstance(instance.airdate, datetime.date))

        #test editing fields without saving, verify changes not present in database
        instance.comment = "added comment"
        instance = plays.objects.get(playID="12345")
        self.assertNotEqual(instance.comment, "added comment")

        #test editing fields with saving, verify changes are present in database
        instance.comment = "added comment"
        instance.save()
        instance = plays.objects.get(playID="12345")
        self.assertEqual(instance.comment, "added comment")
        
    #test generating begin_time and end_time
    def test_play_data_times(self):
        #begin_time = dateTime object of current time - 1 hour
        #end_time = dateTime object of current time

        for testing_timeFrame in range(1, 50):

            #get begin_time, end_time, and json_playData
            begin_time, end_time, json_playData = getPlayData(testing_timeFrame)

            #verify begin_time and end_time are dateTime formatted
            self.assertEqual(True, isinstance(begin_time, datetime.date))
            self.assertEqual(True, isinstance(end_time, datetime.date))

            #verify begin_time is 'testing_timeFrame' hours after end_time
            begin_time_plus_1_hour = begin_time + timedelta(hours = testing_timeFrame)
            self.assertEqual(end_time, begin_time_plus_1_hour)

    #test adding / editing comment to database
    def test_comments(self):

        #create testing POST request
        self.factory = RequestFactory()
        testing_request = self.factory.post("http://www.urlNotImportant-justNeedData.me", data={'commentInput':'newCommentCool'})

        #get our created test insance
        instance = plays.objects.get(playID="12346")

        #add send primary key id of isntance to comment function along with testing_request
        #should add commentInput to instance.pk
        comment(testing_request, instance.pk)

        #get instance again
        instance = plays.objects.get(playID="12346")
        
        #assert that comment has been added
        self.assertEqual(instance.comment, "newCommentCool")

        #test editing comment
        edit_testing_request = self.factory.post("http://www.urlNotImportant-justNeedData.me", data={'commentInput':'edited comment'})
        #add commentInput to instance.pk
        comment(edit_testing_request, instance.pk)

        #get instance again
        instance = plays.objects.get(playID="12346")
        
        #assert that comment has been edited
        self.assertEqual(instance.comment, "edited comment")
    
    #verify kexp json data formatting
    def test_kexp_api_formatting(self):

        #get begin_time, end_time, and json_playData from last 5 hours
        begin_time, end_time, json_playData = getPlayData(5)

        validateSchema(json_playData)


def validateSchema(playData):
    #schema to verify against, written by Martin
    kexp_schema = {
            "type" : "object",
            "properties" : {

                "next" : { "type" : "string" },

                #"previous" : {"type" : None}  #previous is always null ?  

                "results" : {
                    "type" : "array",
                    "items":{
                        "type": "object",
                        "properties":{
                            #playid
                            "playid" : { "type" : "number"},
                            #playtype
                            "playtype" : {
                                "type" : "object",
                                "properties" : {
                                    "playtypeid" : { "type": "number" },
                                    "name" : { "type" : "string" }
                                },
                                "required":[ "playtypeid", "name" ],
                                "additionalProperties": False
                            },
                            #airdate
                            "airdate" : { "type": "string", "format": "date-time" },
                            #epoch_airdate
                            "epoch_airdate" : { "type": "number" },
                            #epoch_airdate_v2
                            "epoch_airdate_v2" : { "type": "string"},
                            #archive_urls
                            "archive_urls": {
                                "type" : "object",
                                "properties" : {
                                    "64":{ "type": "string" },
                                    "32":{ "type": "string" },
                                    "256":{ "type": "string" },
                                    "128":{ "type": "string" },
                                },
                                "required":[ "64", "32", "256", "128"],
                                "additionalProperties": False
                            },
                            #artist can be null (airbreak) or an object (non-airbreak media play)
                            "artist": { 
                                "anyOf": [
                                    {"type": "null"},
                                    {
                                        "type": "object",
                                        "properties":{
                                            "artistid": { "type": "number" },
                                            "name": { "type": "string" },
                                            "islocal": { "type": "boolean" },
                                        },
                                        "required":[ "artistid", "name", "islocal"],
                                        "additionalProperties": False
                                    }
                                ]
                            },
                            #release can be null (airbreak) or an object
                            "release":{
                                "anyOf": [
                                    {"type": "null"},
                                    {
                                        "type": "object",
                                        "properties":{
                                            "releaseid": { "type": "number" },
                                            "name": { "type": "string" },
                                            "largeimageuri": { "type": ["string", "null"] },
                                            "smallimageuri": { "type": ["string", "null"] },
                                        },
                                        "required":[ "releaseid", "name", "largeimageuri", "smallimageuri"],
                                        "additionalProperties": False
                                    }
                                ] 
                            },
                            #releasevent can be null (aircheck) or object
                            "releaseevent":{
                                "anyOf": [
                                    {"type": "null"},
                                    {
                                        "type": "object",
                                        "properties":{
                                            "releaseeventid": { "type": "number" },
                                            "year": { "type": "number" },   
                                        },
                                        "required":[ "releaseeventid", "year"],
                                        "additionalProperties": False
                                    }   
                                ]    
                            },
                            #track can be null (aircheck) or object
                            "track":{
                                "anyOf": [
                                    {"type":"null"},
                                    {
                                        "type":"object",
                                        "properties":{
                                            "trackid": { "type": "number" },
                                            "name": { "type": "string" },   
                                        },
                                        "required":[ "trackid", "name"],
                                        "additionalProperties": False
                                    }
                                ]
                            },
                            #label can be null (aircheck) or object
                            "label":{
                                "anyOf":[
                                    {"type":"null"},
                                    {
                                        "type":"object",
                                        "properties":{
                                            "labelid": { "type": "number" },
                                            "name": { "type": "string" },   
                                        },
                                        "required":[ "labelid", "name"],
                                        "additionalProperties": False
                                    }
                                ]
                            },
                            #comments can be empty[] (aircheck) or object
                            "comments":{
                                "type" : "array",
                                "items":{
                                    "commentid":{ "type":"number"},
                                    "text": {"type":"string"}
                                }
                            },
                            #showid
                            "showid":{"type":"number"}
                        },
                        "required": [ "playid", "playtype", "airdate", "epoch_airdate", "epoch_airdate_v2", "archive_urls", "artist", "release", "releaseevent", "track", "label", "comments", "showid" ],
                        "additionalProperties": False
                    },
                          
                }
                
            },
            "required": [ "next", "previous", "results" ]
        }

    try:
        validate(playData, kexp_schema)
    except jsonschema.ValidationError as e:
        print(e.message)
    except jsonschema.SchemaError as e:
        print(e)





#test with hardcoded jsondata which includes music / airbreak plays

#verify fields present / missing for airbreaks 

#verify fields present / missing for music play

