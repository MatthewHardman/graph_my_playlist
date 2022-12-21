from django.shortcuts import render
from django.shortcuts import redirect
from .models import Playlist

# Create your views here.
def login_view( *args):
    scope = 'playlist-read-private'
    #sp_auth = SpotifyOAuth(scope=scope, client_id='233b08a0708e41e8a3f4956dd52829df',  client_secret='09bea8ddac9b42fcb8d30288919f5f2f', redirect_uri='http://localhost:8000', cache_path='.spotipyoauthcache')
  

def callback_view(request, *args):
    #scope = 'playlist-read-private'
    #sp_auth = SpotifyOAuth(scope=scope, client_id='233b08a0708e41e8a3f4956dd52829df',  client_secret='09bea8ddac9b42fcb8d30288919f5f2f', redirect_uri='http://localhost:8000/callback/')
    #code = request.GET.get('code','')
    #token = sp_auth.get_access_token(code=code)
    #sp = spotipy.Spotify(token)
    #results = Playlist(sp.current_user_playlists(limit=50))
    #results.save()

    return render(request, "callback.html")

