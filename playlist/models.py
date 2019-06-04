from django.db import models

class plays(models.Model):
    #create variables  (when migrated, gets converted to column)
    #django will make another column, a unique id number (primary key, pk) , first album we make will have id =1, second id=2, etc

    playID = models.CharField(max_length=250)
    playtypeID = models.IntegerField(null=True)
    playtypeName = models.CharField(max_length=250)
    artistName = models.CharField(max_length=250, null=True)
    releaseName = models.CharField(max_length=250, null=True)
    releaseImage = models.CharField(max_length=250, null=True)
    trackName = models.CharField(max_length=250, null=True)
    comment = models.CharField(max_length=250, null=True)
    releaseYear = models.CharField(max_length=250, null=True)
    airdate = models.DateTimeField(null=False, blank=False, auto_now_add=False, auto_now=False)

