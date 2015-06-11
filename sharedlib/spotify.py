import requests
from collections import OrderedDict
import json

BASE_URL = 'https://api.spotify.com/v1/'

def search_albums(album=None, artist=None):
    query_items = []
    if album:
        query_items.append(album)
    if artist:
        query_items.append('artist:{}'.format(artist))
    query = ' '.join(query_items)
    params = {'q': query, 'type': 'album', 'limit': 10}
    print '{base}search'.format(base=BASE_URL)
    r = requests.get('{base}search'.format(base=BASE_URL), params=params)
    if r.status_code is 200:
        album_ids = []
        for simplified_album in json.loads(
                r.text, object_pairs_hook=OrderedDict)['albums']['items']:
            album_ids.append(simplified_album['id'])
        if album_ids:
            params = {'ids': ','.join(album_ids)}
            r = requests.get('{base}albums'
                             .format(base=BASE_URL), params=params)
            if r.status_code is 200:
                return {'status': 200,
                        'data': OrderedDict([(album['id'], {
                            'spotify_id': album['id'],
                            'artist': album['artists'][0]['name'],
                            'title': album['name'],
                            'year': int(album['release_date'][:4]),
                            'is_explicit': True in [
                                track['explicit']
                                for track in album['tracks']['items']],
                            'listen_url': album['external_urls']['spotify'],
                            'image_url': album['images'][1]['url'],
                        }) for album in r.json()['albums'] if album['album_type'] == 'album'])}
    return {'status': 404, 'data': {'error': 'No albums found.'}}
