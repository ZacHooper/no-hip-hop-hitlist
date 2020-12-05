import spotipy 
from configs import config
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import csv
import fnmatch

username = '1260769471'
scope = 'playlist-modify-public'
token = util.prompt_for_user_token(username, scope)

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, auth=token)

hitlist_id = '7vFQNWXoblEJXpbnTuyz76'
banned_songs_id = '5QWNXDGREE9hAxddXe2W3m'
no_hiphop_hitlist = '1ahh5eiX08eeiKxxXqZlPp'

playlists = sp.playlist_tracks(hitlist_id)
banned_playlist = sp.playlist_tracks(banned_songs_id)
banned_songs = [item['track']['id'] for item in banned_playlist['items']]

def clean_playlist(playlist_id):
    current_playlist = sp.playlist_tracks(playlist_id)
    current_songs = [item['track']['id'] for item in current_playlist['items']]
    sp.user_playlist_remove_all_occurrences_of_tracks(username, playlist_id, current_songs)

# If returns True the artist is okay, if false remove, if -1 unknown
def check_genre(artist_genres):
    banned_genres = ['hip hop', 'rap', 'trap']
    count = 0 #Counts how many matches there has been

    if artist_genres == []:
        return -1

    for genre in banned_genres:
        filtered = fnmatch.filter(artist_genres, '* ' + genre + '*')
        count += len(filtered)

    if len(artist_genres) != count & count <= 1:
        return True
    else:
        return False

def get_artist_genres(artist_id):
    artist = sp.artist(artist_id)
    return artist['genres']

with open('hitlist.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['Track', 'Artist', 'Genre', 'Genre Status'])
    
    clean_playlist(no_hiphop_hitlist)
    ok_list = []

    for item in playlists['items']:
        track_name = item['track']['name']
        track_id = item['track']['id']
        artist_name = item['track']['artists'][0]['name']
        artist_id = item['track']['artists'][0]['id']
        artist_genres = get_artist_genres(artist_id)

        genre_status = check_genre(artist_genres)

        if not genre_status or track_id in banned_songs:
            print("REMOVED____Track: {} -- Artist: {} -- Genre: {} -- Genre Status: {}".format(track_name, artist_name, artist_genres, genre_status))
            spamwriter.writerow([track_name, artist_name, artist_genres, genre_status])
            continue

        ok_list.append(track_id)

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    results = sp.user_playlist_add_tracks(username, no_hiphop_hitlist, ok_list)
    print(results)
else:
    print("Can't get token for", username)
