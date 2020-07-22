import json, requests
from secrets import TOKEN, UID

class Spotify:
    def __init__(self):
        self.token = TOKEN
        self.user_id = UID
        self.uris = {"uris": []}

    def create_playlist(self, name):
        request_body = {
            "name": name,
            "description": "yt playlist",
            "public": False
        }

        query = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"

        response = requests.post(
            query,
            json=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}"
            }
        )

        response_json = response.json()
        playlist_id = response_json['id']
        return playlist_id

    def get_spotify_uri(self, artist, song_name):
        query = f"https://api.spotify.com/v1/search?query=track%3A{song_name}+artist%3A{artist}&type=track&offset=0&limit=50"

        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}"
            }
        )

        response_json = response.json()
        song = response_json['tracks']['items']
        if not song:
            print(f"{artist}-{song_name} was not found!")
            return None
        else:
            uri = song[0]['uri']
            self.uris['uris'].append(uri)
            return uri

    def add_songs_to_playlist(self, pid, uri_json):
        url = f"https://api.spotify.com/v1/playlists/{pid}/tracks"
        response = requests.post(
            url,
            json=uri_json,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}"
            }
        )
        return response.ok