import requests
import json
import pprint
import datetime

def getTime(header):
    time = requests.get("https://api.spotify.com/v1/me/player", headers=header)
    output = time.json() #json is way easier to deal with
    unixTime = int(output["timestamp"])
    convertedTime = datetime.datetime.fromtimestamp(float(unixTime)/1000).strftime('%H:%M:%S.%f')
    print(convertedTime)

def getTopTracks(header):
    tracks = requests.get("https://api.spotify.com/v1/me/top/tracks",headers=header)
    tracks = tracks.json()
    print(tracks["items"][0]["album"])
token = 'BQAd_XGJwsjrvHzEmHhv59raVmf83M2H5_QNfoHT3h0hgx1volMfc_uWry3Bk2NUlQaXtQ5xlGlZf9S-UmsNbI9pjlRmlLFyNBZoXg-0F0TWrRg0Kkmrxt2plSPldcyOigG2u2nPhBSpRL7yTW_uYa4MvvypCM-gx3ooAs0'
header = {
        'Accept': 'application/json',
        'Content-Type' : 'application/json',
        'Authorization': 'Bearer {}'.format(token)
    }
#getTime(header)
getTopTracks(header)
