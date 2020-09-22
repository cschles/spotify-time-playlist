#!/usr/bin/env python3
import requests
import json
import pprint
import datetime
import re
import os
from urllib.parse import urlencode
from spotipy.oauth2 import SpotifyOAuth

regex = re.compile('(?!.*:).*')


def getAuthorization():
    clientID = os.environ.get('SPOTIPY_CLIENT_ID')
    clientSecret = os.environ.get('SPOTIPY_CLIENT_SECRET')
    uri = 'https://cschles.github.io/spotify-time-playlist/'
    scope = "user-read-playback-state user-top-read user-library-modify playlist-modify-private playlist-modify-public"
    auth=SpotifyOAuth(client_id=clientID,client_secret=clientSecret,redirect_uri=uri,scope=scope)
    tokenStr = auth.get_access_token()
    token = tokenStr['access_token']
    return token

header = {
        'Accept': 'application/json',
        'Content-Type' : 'application/json',
        'Authorization': 'Bearer {}'.format(getAuthorization())
    }

def getTime():
    time = requests.get("https://api.spotify.com/v1/me/player", headers=header)
    output = time.json() 
    unixTime = int(output["timestamp"])
    convertedTime = datetime.datetime.fromtimestamp(float(unixTime)/1000).strftime('%H')
    return convertedTime

def getIDs(tracks):
    ids = []
    for track in tracks:
        id = regex.search(track)
        ids.append(id.group(0))
    return ids
       
def getUri(output,key):
    i = 0
    tracks = []
    while (True):
        try:
            uri = str(output[key][i]["uri"])
            tracks.append(uri)
            i+=1
        except IndexError:
            break
    return tracks

def getTopTracks():
    tracks = requests.get("https://api.spotify.com/v1/me/top/tracks?time_range=medium_term",headers=header)
    toParse = tracks.json()
    topTracks = getUri(toParse,"items")
    return topTracks

def getAudioFeatures(energy,tracks):
    trackIDs = getIDs(tracks)
    trackIDs = ",".join(trackIDs)
    features = requests.get("https://api.spotify.com/v1/audio-features?ids='{}'".format(trackIDs),headers=header)
    audFeat = features.json()
    timely = []
    rec = []
    if energy > .90:
        for i in range(1,18):
            danceability = audFeat["audio_features"][i]['danceability']
            if danceability >= .50:
                track = audFeat["audio_features"][i]['uri']
                id = audFeat["audio_features"][i]['id']
                timely.append(track)
                rec.append(id)
    else:
        for i in range(1,18):
            danceability = audFeat["audio_features"][i]['danceability']
            if danceability < .50:
                track = audFeat["audio_features"][i]['uri']
                id = audFeat["audio_features"][i]['id']
                timely.append(track)
                rec.append(id)
    recs = getRecs(rec,energy)
    timely += recs
    return timely    

def getRecs(seedTracks,energy):
    seed = "%2C".join(seedTracks)
    recs = requests.get("https://api.spotify.com/v1/recommendations?seed_tracks={}&max_energy={}".format(seed,energy),headers=header)
    toParse = recs.json()
    recTracks = getUri(toParse,"tracks")
    return recTracks

def createPlaylist(): 
    info = {
    "name": "A Timely Playlist",
    "description": "A playlist that changes based on the hour",
    "public": 'true'
    }
    r = requests.post("https://api.spotify.com/v1/users/pvmk/playlists",data=json.dumps(info),headers=header)
    output= r.json()
    uri = str(output['id'])
    return uri

def getPlaylist(id):
    playlist = requests.get("https://api.spotify.com/v1/playlists/{}".format(id),headers=header)
    return playlist

def addTracks(playlist,trackIds):
    tracks = "%2C".join(trackIds)
    add = requests.post('https://api.spotify.com/v1/playlists/{}/tracks?uris={}'.format(playlist,tracks),headers=header)
    print(add.content)

def energyLevel(time):
    if 12 < time < 19:
        energy = .90
    else:
        energy = .50
    return energy

def assemblePlaylist(id):
    playlist = getPlaylist(id)
    if playlist.status_code == 404:
        id = createPlaylist()
        print(id)
    tracks = getTopTracks()
    time = int(getTime())
    energy = energyLevel(time)
    recTracks = getAudioFeatures(energy,tracks)
    addTracks(id,recTracks)

def main():
    assemblePlaylist('')
        
if __name__ == "__main__":
    main()
