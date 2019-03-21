import requests
import json
import pprint
import datetime
import re

token = 'BQC2aQpulh7u-TWQjIwWMGHvflnw4amDcyKUvcGjoHRslcmmoigoVgm5pgZY9EAVwoU2oi9gXxoFXKenEj9rPJtBAjzaD73FRaU2oij1Dq59ru428557n_B93vCGDx-xTo_PX6TXN_BPiYt4EnTbYl8OUGxIkvMn-KJkJv1eu7ed63WGyrt23zDKzouQikQBu4Oz09aETupUnr-QFYjVoTwg6uBts-zyQzFeq7va6lK2fA'
header = {
        'Accept': 'application/json',
        'Content-Type' : 'application/json',
        'Authorization': 'Bearer {}'.format(token)
    }
regex = re.compile('[0-9].*\\b')

'''//TODO: 
def getAuthorization():
 #   requests.get('/login', function(req,res))
    scopes = 'user-read-playback-state user-top-read'
}
'''
def getTime(header):
    time = requests.get("https://api.spotify.com/v1/me/player", headers=header)
    output = time.json() 
    unixTime = int(output["timestamp"])
    convertedTime = datetime.datetime.fromtimestamp(float(unixTime)/1000).strftime('%H')
    return convertedTime

def getTracks(output,key):
    i = 0
    tracks = []
    while (True):
        try:
            url = str(output[key][i]["external_urls"])
            id = regex.search(url)
            tracks.append(id.group(0))
            i+=1
        except IndexError:
            break
    return tracks

def getUri(output):
    i = 0
    tracks = []
    while (True):
        try:
            uri = str(output["tracks"][i]["uri"])
            tracks.append(uri)
            i+=1
        except IndexError:
            break
    #print(tracks)
    return tracks

def getTopTracks(header):
    tracks = requests.get("https://api.spotify.com/v1/me/top/tracks?time_range=medium_term&offset=5",headers=header)
    toParse = tracks.json()
    topTracks = getTracks(toParse,"items")
    return topTracks

def getAudioFeatures(tracks,header):
    features = requests.get("https://api.spotify.com/v1/audio-features?ids='{}'".format(tracks),headers=header)
    #print(features.content)
    audFeat = features.json()
    upbeat = []
    slow = []
    test = []
    energy = .00
    for i in range(1,6):
        track = audFeat["audio_features"][i]['id']
        danceability = audFeat["audio_features"][i]['danceability']
        if (danceability) >= .50:
            upbeat.append(track)
        else:
            slow.append(track)
        i+=1
    time = int(getTime(header))
    if 12 < time < 19:
        energy = .90
        recs = getRecs(upbeat,energy)
        test += recs
    else:
        energy = .50
        recs = getRecs(slow,energy)
        test += recs
    #print(upbeat)
    return test

def getRecs(seedTracks,energy):
    seed = "%2C".join(seedTracks)
    recs = requests.get("https://api.spotify.com/v1/recommendations?seed_tracks={}&max_energy={}".format(seed,energy),headers=header)
    toParse = recs.json()
    #print(recs.content)
    recTracks = getUri(toParse)
    return recTracks

def createPlaylist(): #TODO: The Spotify API is currently having issues, so will implement once they update
    info = {
    "name": "A Timely Playlist",
    "description": "A playlist that changes based on the hour",
    "public": 'true'
    }
    r = requests.post("https://api.spotify.com/v1/playlists",data=json.dumps(info),headers=header)
    #print(r)

def getPlaylist(id):
    playlist = requests.get("https://api.spotify.com/v1/playlists/{}".format(id),headers=header)
    return playlist

def addTracks(playlist,trackIds):
    tracks = "%2C".join(trackIds)
    #add = requests.post('https://api.spotify.com/v1/playlists/{}/tracks?uris=spotify:track:5JkCyeCL0S3UqzlibpeDdb'.format(playlist),headers=header)
    #print(tracks)
    add = requests.post('https://api.spotify.com/v1/playlists/{}/tracks?uris={}'.format(playlist,tracks),headers=header)
    print(add.content)


def assemblePlaylist(id):
    playlist = getPlaylist(id)
    if playlist.status_code is 404:
        createPlaylist()
    tracks = getTopTracks(header)
    tracks = ",".join(tracks)
    recTracks = getAudioFeatures(tracks,header)
    print(recTracks)
    addTracks(id,recTracks)

#addTracks("6CUzlkabx0XGnwb9PkbUvn",up)
#getPlaylist('6CUzlkabx0XGnwb9PkbUvn')
assemblePlaylist('6CUzlkabx0XGnwb9PkbUvn')