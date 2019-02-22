import requests
import json
import pprint
import datetime
import re

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
    convertedTime = datetime.datetime.fromtimestamp(float(unixTime)/1000).strftime('%H:%M:%S.%f')
    print(convertedTime)

def getTopTracks(header):
    tracks = requests.get("https://api.spotify.com/v1/me/top/tracks?time_range=medium_term&offset=5",headers=header)
    tracks = tracks.json()
    i = 0
    topTracks = []
    regex = re.compile('[0-9].*\\b')
    while (True):
        try:
            url = str(tracks["items"][i]["external_urls"])
            id = regex.search(url)
            topTracks.append(id.group(0))
            i+=1
        except IndexError:
            break
    return topTracks

def getAudioFeatures(tracks,header):
    features = requests.get("https://api.spotify.com/v1/audio-features?ids='{}'".format(tracks),headers=header)
    #print(features.content)
    audFeat = features.json()
    upbeat = []
    slow = []
    for i in range(1,19):
        track = audFeat["audio_features"][i]['id']
        danceability = audFeat["audio_features"][i]['danceability']
        if (danceability) >= .50:
            upbeat.append(track)
        else:
            slow.append(track)
        i+=1
    print(upbeat)
    print(slow)


token = 'BQAU6YuVWC_nAxj2hyzMvNVA3clrRDUQEvIX0ES5qcMgj89KItGYuVW9NBYHOY3TqE_mja-YnM8qu5ZyXZXBMMEJ-jCoEQjyVcCvEZmZB5GQMlTN3dew2zioSlB9_bmIPMyiBry-76ci648MH0DJy369We4DO4jS8gX_YOg'
header = {
        'Accept': 'application/json',
        'Content-Type' : 'application/json',
        'Authorization': 'Bearer {}'.format(token)
    }
getTime(header)
tracks = getTopTracks(header)
tracks = ",".join(tracks)
getAudioFeatures(tracks,header)

