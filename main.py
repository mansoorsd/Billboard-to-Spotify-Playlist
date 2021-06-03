import spotipy
from bs4 import BeautifulSoup
import requests
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

URL = "https://www.billboard.com/charts/hot-100/"

Client_ID = ""
Client_Secret = ""
# Input from console
date = input("What year you want to travel to? Enter the date in the following format YYYY-MM-DD: ")

# Getting Song List from Billboard
response = requests.get(URL + date)
soup = BeautifulSoup(response.text, "html.parser")
song_list = soup.findAll(name="span", class_="chart-element__information__song text--truncate color--primary")
song_names = [song.getText() for song in song_list]

# Authenticating Spotify
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com/callback/",
        client_id=Client_ID,
        client_secret=Client_Secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

# Getting song uri's from spotify
song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        pass
        # print(f"{song} doesn't exist in Spotify. Skipped.")


# Creating a playlist with song uri's
playlist = sp.user_playlist_create(user=user_id, name=f"{date} 100 BILLBOARD", public=False)
print(playlist)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
