import sys
import spotipy
import pprint
from spotipy.oauth2 import SpotifyClientCredentials


if len(sys.argv) > 1:
    search_str = sys.argv[1]
else:
    search_str = 'Radiohead'


client_id = "a1b468cc979f494dbbb271d2aba7ab34"
client_secret = "3a8d593557604dba865efc89b13b3b54"
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_tracks(data):
	tracks=data["tracks"]
	names=[]
	for track in tracks:
		title=track["name"]
		names.append(title)
	return names

def callApi(music):
	result = sp.recommendations(seed_genres=music, limit=20, country='IE')
	#result=result[0]
	names=get_tracks(result)
	return names


