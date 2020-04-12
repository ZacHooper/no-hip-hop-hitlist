import spotipy
from configs import config
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

hitlist_id = '7vFQNWXoblEJXpbnTuyz76'
test_id = '19fVvXqXq8KUpK3MtNIIxJ'

playlists = sp.playlist_tracks(hitlist_id)
track_name = playlists['items'][0]['track']['name']
album_name = playlists['items'][0]['track']['album']['name']
album_id = playlists['items'][0]['track']['album']['id']
artist1_name = playlists['items'][0]['track']['artists'][0]['name']
artist1_id = playlists['items'][0]['track']['artists'][0]['id']

def get_artist_genres(artist_id):
    artist = sp.artist(artist_id)
    return artist['genres']

for item in playlists['items']:
    track_name = item['track']['name']
    artist_name = item['track']['artists'][0]['name']
    artist_id = item['track']['artists'][0]['id']
    artist_genres = get_artist_genres(artist_id)
    print("Track: {} -- Artist: {} -- Genre: {}".format(track_name, artist_name, artist_genres))






