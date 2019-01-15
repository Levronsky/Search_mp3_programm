import os
import re
import sys
from itertools import groupby
from tinytag import TinyTag


def main():
    """Start searching music by artist."""
    directory = 'music'
    artist_name = sys.argv[1]
    list_of_songs = get_all_music(directory)
    music_with_all_tags = (
        get_music_with_all_tags(list_of_songs)
        )
    artist_songs = search_songs_by_artist(
        artist_name, music_with_all_tags
        )
    artist_albums = group_by_albums(artist_songs)
    print_songs(artist_albums)


def get_all_music(directory):
    """Create a list of all songs."""
    list_of_songs = []
    for root, dirs, names in os.walk(directory):
        for name in names:
            song_path = os.path.join(root, name)
            if re.search('.mp3$', song_path):
                list_of_songs.append(song_path)
    return list_of_songs


def get_music_with_all_tags(list_of_songs):
    """Create a list of tags for each song."""
    music_with_all_tags = [
        TinyTag.get(song) for song in list_of_songs
        ]
    return music_with_all_tags


def search_songs_by_artist(artist_name, music_with_all_tags):
    """Create a list of songs of the desired artist."""
    artist_songs = []
    for song in music_with_all_tags:
        artist_name = artist_name.lower()
        song.artist = str(song.artist).lower()
        if song.artist == artist_name:
            artist_songs.append(song)
    return artist_songs


def group_by_albums(artist_songs):
    """Group songs by album.
    
    The function creates a dictionary where:
    key is the name of the album
    value - the list of songs of this album.
    """
    artist_albums = {
        album: list(group) for album, group 
        in groupby(artist_songs, lambda tag: tag.album)
    }
    return artist_albums


def print_songs(artist_albums):
    """Print songs by album."""
    for album, songs in artist_albums.items():
        print(album + ':\n')
        for song in songs:
            print("Название:", song.title)
            print("Альбом:", song.album)
            print("Исполнитель:", song.artist, '\n')


if __name__ == '__main__':
    main()
