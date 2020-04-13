import spotipy
from configs import config
from spotipy.oauth2 import SpotifyClientCredentials
import csv
import fnmatch

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

hitlist_id = '7vFQNWXoblEJXpbnTuyz76'
test_id = '19fVvXqXq8KUpK3MtNIIxJ'
genre_test_id = '5QWNXDGREE9hAxddXe2W3m'

playlists = sp.playlist_tracks(hitlist_id)

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
    spamwriter.writerow(['Track', 'Artist', 'Genre'])
    
    ok_list = []

    for item in playlists['items']:
        track_name = item['track']['name']
        artist_name = item['track']['artists'][0]['name']
        artist_id = item['track']['artists'][0]['id']
        artist_genres = get_artist_genres(artist_id)
        genre_status = check_genre(artist_genres)
        print("Track: {} -- Artist: {} -- Genre: {} -- Genre Status: {}".format(track_name, artist_name, artist_genres, genre_status))
        if not genre_status:
            spamwriter.writerow([track_name, artist_name, artist_genres, genre_status])
            continue
        ok_list.append(track_name)


