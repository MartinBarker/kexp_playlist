from django.db import models

class plays(models.Model):
    #every mode or blueprint u create has to inherit from models.Model
    #create variables  (when migrated, gets converted to column)
    #need to tell django what type of value this variable will hold
    
    playID = models.CharField(max_length=250)
    playtypeID = models.IntegerField(null=True)
    playtypeName = models.CharField(max_length=250)
    
    airdate = models.DateTimeField(null=False, blank=False, auto_now_add=False, auto_now=False)
    #airdate =  models.CharField(max_length=250, null=True)

    artistName = models.CharField(max_length=250, null=True)
    releaseName = models.CharField(max_length=250, null=True)
    releaseImage = models.CharField(max_length=250, null=True)
    
    #releaseYear = models.DateField(null=True, blank=False, auto_now_add=False, auto_now=False)
    releaseYear = models.CharField(max_length=250, null=True)

    trackName = models.CharField(max_length=250, null=True)
    comment = models.CharField(max_length=250, null=True)
    
    #django will make another column, a unique id number (primary key, pk) , first album we make will have id =1, second id=2, etc

    #built in syntax : string representation of this object (specify what its supposed ot print out)
    #def __str__(self):
    #    return str(self.pk) + ' - ' + self.trackName

