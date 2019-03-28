import requests
import json
import pprint
import datetime
import re

token = 'BQBxuXjxfEBVuwoDGS30uzxH-EFSddBS-vdmUBeyQllPTkGxoTKkbOOiVPE6CIfloOk_UB85qdi-uuBqZHO3_GtgScoZREzZt4j9WtGmkxkZNr2wnl7VakhANN6yxxEb0wem-2a6uL6K031iE8-aKOXvLP_uCcpN4mSzJS6lwv0lzSoW1F2AJBLiUohohoUhc4_1Wci_SMi2N3VgvyjO76Sc3VykPtK63Dr80yyBt7YLaw'
header = {
        'Accept': 'application/json',
        'Content-Type' : 'application/json',
        'Authorization': 'Bearer {}'.format(token)
    }

regex = re.compile('(?!.*:).*')
'''//TODO: 
def getAuthorization():
 #   requests.get('/login', function(req,res))
    scopes = 'user-read-playback-state user-top-read'
}
'''
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
    #print(recs.content)
    recTracks = getUri(toParse,"tracks")
    return recTracks

def createPlaylist(): #TODO: The Spotify API is currently having issues, so will implement once they update
    info = {
    "name": "A Timely Playlist",
    "description": "A playlist that changes based on the hour",
    "public": 'true'
    }
    r = requests.post("https://api.spotify.com/v1/playlists",data=json.dumps(info),headers=header)
    print(r)

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
    if playlist.status_code is 404:
        createPlaylist()
    tracks = getTopTracks()
    time = int(getTime())
    energy = energyLevel(time)
    recTracks = getAudioFeatures(energy,tracks)
    addTracks(id,recTracks)

assemblePlaylist('6CUzlkabx0XGnwb9PkbUvn')
