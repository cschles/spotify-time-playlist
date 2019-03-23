import requests
import json
import pprint
import datetime
import re

token = 'BQBN_f6WYwdMJCKrc5cbiPXmL6XhMILSbrZMFAf0eCYN_UXGvTOkOzrzdZ4GfoonKenDj4ANLECyBLc32CohTCcWRNlGW5mTjw70T4DbFpjpXKYCH4V0pEOtPSuex5qXkXIEGqQ9bZa9CZp6rM6kXuOeD8nTMYhRSCB2PaSocukPleEvJVSCBcUuUABpikQemJfIVySpkAs3z2n-rakVluegoPUnPjrZc93V38Oxfq0SsQ'
header = {
        'Accept': 'application/json',
        'Content-Type' : 'application/json',
        'Authorization': 'Bearer {}'.format(token)
    }
#regex = re.compile('[0-9].*\\b')
regex = re.compile('(?!.*:).*')
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



def getTopTracks(header):
    tracks = requests.get("https://api.spotify.com/v1/me/top/tracks?time_range=medium_term&limit=6",headers=header)
    toParse = tracks.json()
    topTracks = getUri(toParse,"items")
    return topTracks

def getAudioFeatures(tracks,header):
    #TODO: Go through and check when spotify:track is needed and when just the track id is needed. Probably need to rethink how this is set up
    trackIDs = getIDs(tracks)
    trackIDs = ",".join(trackIDs)
    features = requests.get("https://api.spotify.com/v1/audio-features?ids='{}'".format(trackIDs),headers=header)
    audFeat = features.json()
    upbeat = []
    slow = []
    timely = []
    energy = .00
    time = int(getTime(header))
    #if 12 < time < 19:
    for i in range(1,5):
        track = audFeat["audio_features"][i]['id']
        danceability = audFeat["audio_features"][i]['danceability']
        if (danceability) >= .50:
            upbeat.append(track)
        else:
            slow.append(track)
    #print(upbeat)
    time = int(getTime(header))
    if 12 < time < 19:
        energy = .90
        recs = getRecs(upbeat,energy)
        timely += upbeat
        timely += recs
    else:
        energy = .50
        recs = getRecs(slow,energy)
        timely += slow
        timely += recs
    #print(upbeat)
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
    #tracks = ",".join(tracks)
    #print(tracks)
    recTracks = getAudioFeatures(tracks,header)
    #print(recTracks)
    addTracks(id,recTracks)

#addTracks("6CUzlkabx0XGnwb9PkbUvn",up)
#getPlaylist('6CUzlkabx0XGnwb9PkbUvn')
assemblePlaylist('6CUzlkabx0XGnwb9PkbUvn')
