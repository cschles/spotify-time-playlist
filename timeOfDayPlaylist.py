import requests
import json
import pprint
import datetime
import re

token = 'BQCrpsucaykrF_a05ylQsHIyQkA250993Z083W1msxBsajqUzLg6kJnnipeHovIZfa25VV1j_jFCYVZAErRBSdI2JOgWiFbaNSMDT7v1gXMeKK-YErswamcVp_hmSuvcItvcRkjcOeGFl7_ZbyjGFOv4zfzKPAwyAjtdADpZVPFP9CEAld9oZCdJjcD847QqCRsXMW448M23Z-826LVxtcJn0rE30RSZHo4RbBi0sc5P'
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

def getTopTracks(header):
    tracks = requests.get("https://api.spotify.com/v1/me/top/tracks?time_range=medium_term&offset=5",headers=header)
    toParse = tracks.json()
    i = 0
    topTracks = getTracks(toParse,"items")
    return topTracks

def getAudioFeatures(tracks,header):
    features = requests.get("https://api.spotify.com/v1/audio-features?ids='{}'".format(tracks),headers=header)
    #print(features.content)
    audFeat = features.json()
    upbeat = []
    slow = []
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
        upbeat += recs
    else:
        energy = .50
        recs = getRecs(slow,energy)
        slow += recs
    #print(upbeat)
    return upbeat

def getRecs(seedTracks,energy):
    seed = "%2C".join(seedTracks)
    recs = requests.get("https://api.spotify.com/v1/recommendations?seed_tracks={}&max_energy={}".format(seed,energy),headers=header)
    toParse = recs.json()
    #print(recs.content)
    recTracks = getTracks(toParse,"tracks")
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
    print(playlist.content)

def addTracks(playlist,trackIds):
    tracks = "spotify:track:".join(trackIds)
    add = requests.post('https://api.spotify.com/v1/playlists/{}/tracks?uris={}'.format(playlist,tracks),headers=header)

tracks = getTopTracks(header)
tracks = ",".join(tracks)
up = getAudioFeatures(tracks,header)
addTracks("6CUzlkabx0XGnwb9PkbUvn",up)
#getPlaylist('6CUzlkabx0XGnwb9PkbUvn')