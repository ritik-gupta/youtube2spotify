from youtube import Youtube
from spotify import Spotify

def main():
    playlist_url = input("Youtube playlist url: ")
    playlist_name = input("Playlist name: ")

    yt = Youtube(playlist_url)
    song_titles = yt.get_songs_title()
    print(len(song_titles))
    songs_info = yt.get_songs_info(song_titles)
    print(len(songs_info))
    spotify = Spotify()
    playlst_id = spotify.create_playlist(playlist_name)

    for song_name, artist in songs_info.items():
        uri = spotify.get_spotify_uri(artist, song_name)
        status = spotify.add_songs_to_playlist(playlst_id, {"uris": [uri]})
        if status:
            print(f"{artist}-{song_name} was added to playlist.")
        else:
            print(f"\nERROR!! {artist}-{song_name} could not be added.\n")

if __name__ == "__main__":
    main()