from django.shortcuts import render
from .models import SpotifyUserPlaylist
from spotify.views import execute_spotify_api_request
import math
from collections import Counter
import json

# Create your views here.

def login_view(request):
    return render(request, 'login.html')

def callback_view(request, pk):
    #pk is passed through the URL and is the access_token
    #get current user and display name
    current_user = execute_spotify_api_request(pk, 'me')
    display_name = current_user['display_name']
    spotify_id = current_user['id']
    #get current user's playlists - can only get 50 at a time. 
    playlist_names = []
    playlist_id = []
    playlist_img = []
    requested = 0
    playlist_dictionary={}
    while True:

        temp_playlist_dictionary = execute_spotify_api_request(pk, 'me/playlists?offset='+str(requested)+'&limit=50')
        

        for index in range(len(temp_playlist_dictionary['items'])):
            playlist_names.append(temp_playlist_dictionary['items'][index]['name'])
            playlist_id.append(temp_playlist_dictionary['items'][index]['id'])
            try:
                playlist_img.append(temp_playlist_dictionary['items'][index]['images'][0]['url'])
            except: 
                playlist_img.append('http://goo.gl/vyAs27')
            
        playlist_dictionary.update(temp_playlist_dictionary)
        requested += 50
        total = temp_playlist_dictionary['total']

        if total<=requested:
            break
    
    #Save playlist information to database with access token and user ID
    SpotifyPlaylists = SpotifyUserPlaylist.objects.filter(user=spotify_id)

    if not SpotifyPlaylists.exists():
        SpotifyPlaylists = SpotifyUserPlaylist(user = spotify_id, access_token = pk, playlist = playlist_dictionary)
        SpotifyPlaylists.save()
    
    else:
        SpotifyPlaylists.update(user = spotify_id, access_token = pk, playlist = playlist_dictionary)

    context = {
        'display_name': display_name,
        'playlist_values': zip(playlist_names, playlist_id, playlist_img),
        'spotify_id': spotify_id
    }
            
    return render(request, 'callback.html', context)

def playlist_view(request, id):
    spotify_id = request.GET.get('user')
    access_token = SpotifyUserPlaylist.objects.get(user=spotify_id).access_token

    requested = 0
    tracks_dictionary = {}
    track_name = []
    track_id = []

#Use playlist ID to get all the songs on the playlist. Store track name and Id. 
    while True:

        temp_tracks_dictionary = execute_spotify_api_request(access_token, 'playlists/'+id+'/tracks?offset='+str(requested)+'&limit=50&fields=total,items(track(name,id))')

        for index in range(len(temp_tracks_dictionary['items'])):
            track_name.append(temp_tracks_dictionary['items'][index]['track']['name'])
            track_id.append(temp_tracks_dictionary['items'][index]['track']['id'])

        tracks_dictionary.update(temp_tracks_dictionary)
        requested += 50
        total = temp_tracks_dictionary['total']
       
        if total<=requested:
            break
    

    #Parse the track Ids into strings, 100 ids long to be passed to Spotify Audio Features API store in track_call_lst
    track_call_lst = []
    for i in range(0, len(track_id), 100):
        track_call_string = ''
        inner_track_lst = track_id[i:i+100]
        for j in inner_track_lst:
            track_call_string = track_call_string + j +','
        track_call_string = track_call_string.rstrip(',')
        track_call_lst += [track_call_string]

    acousticness_lst = []
    danceability_lst = []
    energy_lst = []
    duration_lst = []
    tempo_lst = []
    valence_lst = []

#Use track_call_lst to get audio features of songs
    for i in track_call_lst:
        track_audio_dictionary = execute_spotify_api_request(access_token, 'audio-features?ids='+i)
        for index in range(len(track_audio_dictionary['audio_features'])):
            try:
                acousticness_lst.append(track_audio_dictionary['audio_features'][index]['acousticness'])
                danceability_lst.append(track_audio_dictionary['audio_features'][index]['danceability'])
                energy_lst.append(track_audio_dictionary['audio_features'][index]['energy'])
                duration_lst.append(track_audio_dictionary['audio_features'][index]['duration_ms'])
                tempo_lst.append(track_audio_dictionary['audio_features'][index]['tempo'])
                valence_lst.append(track_audio_dictionary['audio_features'][index]['valence'])
            except:
                print(track_audio_dictionary['audio_features'][index])

#Get genre and popularity information from individual songs. 
   # genre_lst = []
   # popularity_lst = []
   # for i in track_id:
   #     track_info_dictionary = execute_spotify_api_request(access_token, 'tracks/'+i)
    #    artist_id = track_info_dictionary['artists'][0]['id']
    #    artist_dictionary = execute_spotify_api_request(access_token,'artists/'+artist_id)
     #   genre_lst.extend(artist_dictionary['genres'])
     #   popularity_lst.append(track_info_dictionary['popularity'])

   # genre_Counter = Counter(genre_lst)
   # genre_tuple = genre_Counter.most_common()

  #  ordered_genre_lst_raw = []
   # ordered_genre_count_raw = []
   # for i in genre_tuple:
    #    ordered_genre_lst_raw.append(i[0])
    #    ordered_genre_count_raw.append(i[1])

   # ordered_genre_lst = json.dumps(ordered_genre_lst_raw)
   # ordered_genre_count = json.dumps(ordered_genre_count_raw)

    context = {
        'acousticness': find_average(acousticness_lst),
        'danceability': find_average(danceability_lst),
        'energy': find_average(energy_lst),
        'duration': ms_to_min_sec(find_average(duration_lst)),
        'tempo': find_average(tempo_lst),
        'valence': find_average(valence_lst),
      #  'popularity': find_average(popularity_lst),
      #  'genre_names':ordered_genre_lst,
      #  'genre_count': ordered_genre_count
    }
    
    
      
    return render(request, 'playlist.html', context)

def find_average(lst):
    sum = 0
    for i in lst:
        sum += i
    average = round(sum/len(lst), 2)
    return average

def ms_to_min_sec(millis):
    millis = int(millis)
    seconds = (millis/1000)%60
    seconds = int(seconds)
    minutes = (millis/(1000*60))%60
    minutes = int(minutes)

    return("%d:%d" % (minutes, seconds))
