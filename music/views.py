from django.shortcuts import render
#from django.http import HttpResponse
from .models import Album, Song
from django.shortcuts import render, get_object_or_404
from django.http import Http404

def index(request):
    #get all albums objects in database
    all_albums = Album.objects.all()
    html = ''
    #template = loader.get_template('music/index.html') #django automatically looks for templates folder in app directory
    #pass album info in to template through dictionary
    context = { 'all_albums': all_albums }


    #for album in all_albums:
    #    url = '/music/' + str(album.id) + '/'
    #    html += '<a href="' + url + '"> ' + album.album_title +'</a><br> '

    #pass this infointo template
    #return HttpResponse(template.render(context, request)) 

    #converts to valid http response
    return render(request, 'music/index.html', context)

def detail(request, album_id):
    #try to query database for valid id
    try:
        album = Album.objects.get(pk=album_id)
    except Album.DoesNotExist:
        raise Http404("album does not exist in db")
    
    #return HttpResponse("<h2>details for album id: " + str(album_id) + " </h2>")
    return render(request, 'music/detail.html', {'album': album})

def favorite(request, album_id):
    print("inside views.py favorite funvtion")
    #return render(request, 'music/detail.html', {'album': album})
    album = get_object_or_404(Album, pk=album_id)
    #make sure we have valid song id
    #set is_favorite =true for song in db, if it doesnt exist, send back error message
    try:
        #get the value of whatever song they selected
        selected_song = album.song_set.get(pk=request.POST['song'])
    
    except (KeyError, Song.DoesNotExist):
        return render(request, 'music/detail.html', { 'album':album, 'error_message':'You did not select a valid song' })
    
    else:
        selected_song.is_favorite = True 
        selected_song.save() #stores changes in database
        return render(request, 'music/detail.html', {'album': album})