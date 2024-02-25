import requests
import dotenv
import os

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