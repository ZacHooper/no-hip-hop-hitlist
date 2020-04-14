import sys
import spotipy
import spotipy.util as util
from configs import config

no_hiphop_hitlist = '1ahh5eiX08eeiKxxXqZlPp'
scope = 'user-library-read playlist-modify-public'

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()

token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_saved_tracks()
    for item in results['items']:
        track = item['track']
        print(track['name'] + ' - ' + track['artists'][0]['name'])
else:
    print("Can't get token for", username)

def clean_playlist(playlist_id):
    current_playlist = sp.playlist_tracks(playlist_id)
    current_songs = [item['track']['id'] for item in current_playlist['items']]
    sp.user_playlist_remove_all_occurrences_of_tracks(username, playlist_id, current_songs)