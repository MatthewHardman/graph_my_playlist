from django.shortcuts import render, redirect
from decouple import config
from rest_framework.views import APIView
from requests import Request, post, get
from rest_framework import status
from rest_framework.response import Response
from .models import SpotifyToken

# Create your views here.
class AuthURL(APIView):
    def get(self, request, format=None):
        scopes = 'playlist-read-private playlist-read-collaborative user-read-email'

        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes, 
            'response_type': 'code',
            'redirect_uri': config('REDIRECT_URI'), 
            'client_id': config('CLIENT_ID')
        }).prepare().url

        return Response({'url': url}, status=status.HTTP_200_OK)

def spotify_callback(request, format=None):
    code = request.GET.get('code')
    error = request.GET.get('error')
    

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code, 
        'redirect_uri': config("REDIRECT_URI"),
        'client_id': config('CLIENT_ID'),
        'client_secret': config('CLIENT_SECRET'),
    }).json()

    access_token = response.get('access_token')
    #token_type = response.get('token_type')
    #refresh_token = response.get('refresh_token')
    error = response.get('error')

    #user = execute_spotify_api_request(access_token, 'me')
  
    #tokens = SpotifyToken.objects.filter(user=user)

    #if not tokens.exists():
        #tokens = SpotifyToken(user=user, access_token=access_token, refresh_token=refresh_token, token_type=token_type)
        #tokens.save()
    

    return redirect('../pages/callback/'+access_token)



def execute_spotify_api_request(access_token, endpoint):
    headers = {'Content-Type': 'application/json', 'Authorization':'Bearer '+access_token}

    response = get('https://api.spotify.com/v1/'+endpoint, {}, headers=headers)

    try:
         return response.json()
    except:
        return{'Error: Could not process request'}







def refresh_spotify_token(user):
    refresh_token = SpotifyToken.objects.filter(user=user).refresh_token

    response = post('https://accounts/spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh-token':refresh_token,
        'client_id': config('CLIENT_ID'),
        'client_secret': config('CLIENT_SECRET'),
    })
    
    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')

    tokens = SpotifyToken(user=user, access_token=access_token, refresh_token=refresh_token, token_type=token_type)
    tokens.save()