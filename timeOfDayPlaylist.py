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

token = 'BQDtmExWTg51Moxd6EtQyMJJvB5bDD-MvzG2ePXhvdWyF4U23r6EPCVn6UAGKym-AL3yeg4P44YiqO7_DF_sKkbkQ2eYoyOzlTOlUAotLMZxZuJBq-sJYSNOOh3L-2duX0uWtqeO9oMJr5_b7tWvTMXOnYIHJQp3zW6mwKk'
header = {
        'Accept': 'application/json',
        'Content-Type' : 'application/json',
        'Authorization': 'Bearer {}'.format(token)
    }
#getTime(header)
tracks = getTopTracks(header)
print(tracks)
