# AUtheticatication

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id= 'client_id from Spotify', client_secret='secret code from Spotify')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#  Extract the list of artists
import pandas as pd
df_artist = pd.read_excel('Artists_name.xlsx')
naija_artist=df_artist['artist']
naija_artist= list(naija_artist)

#  Create empty list for artist name and ID

artist_id= []
artist_name =[]

# Iterate through the list naija_artist and search for artist name

for artist in naija_artist:
    get_artist_id= sp.search(q=artist, type='artist')


#     print each artist name to be sure you have the rigt artist name

    print(get_artist_id['artists']['items'][0]['name'])

#      Append artist name and artist ID

    artist_id.append(get_artist_id['artists']['items'][0]['id'])
    artist_name.append(get_artist_id['artists']['items'][0]['name'])

    # converting artist name and ID to Dataframe
d1 = pd.DataFrame(artist_id,columns = ['Artist id'])
d2 = pd.DataFrame(artist_name,columns = ['Artist name'])

# concatinate the Name and ID dataframes and saving
d3= pd.concat([d1, d2], axis=1)

d3.to_csv('ArtistID_22')


# GEtting all songs by artists

artist_info = pd.read_csv('ArtistID1.csv')

# get artist album

artist_id= list(artist_info['Artist id'])

spotify_artist_album ={}


# spotify_artist_album = {}

spotify_artist_album['AlbumName'] = []
spotify_artist_album['uri_Album'] = []

spotify_artist_album['artistID'] = []
spotify_artist_album['album_date'] = []



for artistid in artist_id:
    artist_album= sp.artist_albums(artist_id=artistid, limit=45,album_type='album' )
    for i in range(len(artist_album['items'])):
        spotify_artist_album['artistID'].append(artistid)
        spotify_artist_album['AlbumName'].append(artist_album['items'][i]['name'])
        spotify_artist_album['uri_Album'].append(artist_album['items'][i]['uri'])
        spotify_artist_album['album_date'].append(artist_album['items'][i]['release_date'])

album_df= pd.DataFrame.from_dict(spotify_artist_album)
album_df.head()

# getting songs from album
album_uri = list(album_df['uri_Album'])
albums_Tracks={}

# albums_Tracks['album'] = []
albums_Tracks['track_number'] = []
albums_Tracks['track_id'] = []
albums_Tracks['track_name'] = []
albums_Tracks['Album_uri'] = []

for uri in album_uri:
    trackss=sp.album_tracks(uri, limit=49)
    for i in range(len(trackss['items'])):
        albums_Tracks['Album_uri'].append(uri)

        albums_Tracks['track_number'].append(trackss['items'][i]['track_number'])
        albums_Tracks['track_id'].append(trackss['items'][i]['id'])
        albums_Tracks['track_name'].append(trackss['items'][i]['name'])

# print(albums_Tracks)
tracks_id= pd.DataFrame.from_dict(albums_Tracks)

# getting the track Features

track_ID= list(tracks_id['track_id'])
import time
import numpy as np

audioFeatures={}
    #Add new key-values to store audio features
audioFeatures['track_idd']=[]
audioFeatures['acousticness'] = []
audioFeatures['danceability'] = []
audioFeatures['energy'] = []
audioFeatures['instrumentalness'] = []
audioFeatures['liveness'] = []
audioFeatures['loudness'] = []
audioFeatures['speechiness'] = []
audioFeatures['tempo'] = []
audioFeatures['valence'] = []
audioFeatures['popularity'] = []
audioFeatures['duration_ms'] = []
audioFeatures['time_signature'] = []

sleep_min = 2
sleep_max = 5
start_time = time.time()
request_count = 0
    #create a track counter
track_count = 0
for tracks in track_ID:

    #pull audio features per track
    features = sp.audio_features(tracks)

    #Append to relevant key-value
    audioFeatures['track_idd'].append(tracks)
    audioFeatures['acousticness'].append(features[0]['acousticness'])
    audioFeatures['danceability'].append(features[0]['danceability'])
    audioFeatures['energy'].append(features[0]['energy'])
    audioFeatures['instrumentalness'].append(features[0]['instrumentalness'])
    audioFeatures['liveness'].append(features[0]['liveness'])
    audioFeatures['loudness'].append(features[0]['loudness'])
    audioFeatures['speechiness'].append(features[0]['speechiness'])
    audioFeatures['tempo'].append(features[0]['tempo'])
    audioFeatures['valence'].append(features[0]['valence'])
    audioFeatures['duration_ms'].append(features[0]['duration_ms'])
    audioFeatures['time_signature'].append(features[0]['time_signature'])
    #popularity is stored elsewhere
    pop = sp.track(tracks)
    audioFeatures['popularity'].append(pop['popularity'])
    # set timing
    track_count+=1
    request_count+=1
    if request_count % 100 == 0:
        print(str(request_count) + " track completed")
        time.sleep(np.random.uniform(sleep_min, sleep_max))
        print('Loop #: {}'.format(request_count))
        print('Elapsed Time: {} seconds'.format(time.time() - start_time))
audio_Features_df= pd.DataFrame.from_dict(audioFeatures)

# Merging artist_info and album_df
spotify_all_info= artist_info.merge(album_df, left_on='Artist id', right_on='artistID').merge(tracks_id, left_on='uri_Album',right_on='Album_uri').merge(audio_Features_df, left_on='track_id', right_on='track_idd')

spotify_all_info.info()
spotify_all_info.to_csv('spotify_all_info.csv')
audio_Features_df.to_csv('audio_Features.csv')
tracks_id.to_csv('tracks_id.csv')
album_df.to_csv('album_info.csv')
