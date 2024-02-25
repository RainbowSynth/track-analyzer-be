import requests
import dotenv
import os
from urllib.parse import urlencode
import imageio
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

dotenv.load_dotenv(".env")
client_id = os.environ['SPOTIFY_ID']
client_secret = os.environ['SPOTIFY_SECRET']

def get_spotify_access_token(client_id, client_secret):
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })
    auth_response_data = auth_response.json()
    return auth_response_data['access_token']

def analyze_album_cover(track_id):
    access_token = get_spotify_access_token(client_id, client_secret)
    search_url = f'https://api.spotify.com/v1/tracks/{track_id}'
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    album_art = requests.get(search_url, headers=headers).json()['album']['images'][0]['url']
    image = Image.open(imageio.imread(album_art))
    
    # Convert the image to RGB
    image = image.convert('RGB')
    
    # Resize the image to reduce processing time, maintaining aspect ratio
    aspect_ratio = image.height / image.width
    new_height = int(10 * aspect_ratio)
    image = image.resize((10, new_height))
    
    # Convert the image data to a list of RGB values
    pixels = np.array(image).reshape(-1, 3)
    
    # Use KMeans clustering to find main colors
    kmeans = KMeans(n_clusters=2)
    kmeans.fit(pixels)
    
    # The cluster centers are our main colors
    main_colors = kmeans.cluster_centers_
    
    # Convert to integers, since RGB values should be integers
    main_colors = main_colors.round().astype(int).tolist()
    
    return main_colors


def get_analysis(track_id):
    access_token = get_spotify_access_token(client_id, client_secret)
    search_url = f'https://api.spotify.com/v1/audio-analysis/{track_id}'
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    response = requests.get(search_url, headers=headers)
    return response.json()

def get_loudness_change(segments):
    durations = [segment['start'] for segment in segments]
    loudness = [(segment['loudness_start'] + segment['loudness_end']) / 2 for segment in segments]
    pitches = [segment['pitches'] for segment in segments]
    return durations, loudness, pitches

def analyze_track(track_details):
    segments = track_details.get('segments')
    durations, loudness, pitches = get_loudness_change(segments)
    return {
        "durations": durations,
        "loudness": loudness,
        "pitches": pitches
    }

def get_id_from_name(track_name):
    access_token = get_spotify_access_token(client_id, client_secret)
    params = {
        'q': track_name,
        'type': 'track',
        'limit': 1,
    }
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    search_url = 'https://api.spotify.com/v1/search?' + urlencode(params)
    response = requests.get(search_url, headers=headers)
    response_data = response.json()
    track_id = response_data['tracks']['items'][0]['id'] if response_data['tracks']['items'] else None
    return {
        "track_id": track_id
    }
