from django.db import models

class Album(models.Model):
    #every mode or blueprint u create has to inherit from models.Model
    #create variables  (when migrated, gets converted to column)
    #need to tell django what type of value this variable will hold
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    album_logo = models.CharField(max_length=1000)
    #django will make another column, a unique id number (primary key, pk) , first album we make will have id =1, second id=2, etc

    #built in syntax : string representation of this object (specify what its supposed ot print out)
    def __str__(self):
        return self.album_title + ' - ' + self.artist



class Song(models.Model):
    #each song needs to be associated with an album, foreignKey tells song that album var points to primarykey of album object, on_delete=models.cascade means that if linked album is deleted, the foreignKey linked songs will also be deleted 
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=10)
    song_title = models.CharField(max_length=250)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.song_title