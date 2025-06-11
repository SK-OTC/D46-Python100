import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
from config import USERNAME, SECRET, KEY

key = KEY
# THEY ARE DIFFERENT VALUES
secret = SECRET

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        client_id=key,
        client_secret=secret,
        redirect_uri="http://example.com",
        cache_path="token.txt",
        username=USERNAME))
user = sp.current_user()["id"]
time_traveler = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{time_traveler}")
read = response.text

soup = BeautifulSoup(read, "html.parser")

rankings = soup.find_all(name="span",
                         class_="c-label a-font-primary-bold-l u-font-size-32@tablet u-letter-spacing-0080@tablet")

number_list = [int(num.getText()) for num in rankings]
first_title = soup.find(name="a", href="#", class_="c-title__link lrv-a-unstyle-link")

titles = soup.find_all(name="h3", id="title-of-a-story", class_="c-title a-no-trucate a-font-primary-bold-s"
                                                                " u-letter-spacing-0021 lrv-u-font-size-18@tablet"
                                                                " lrv-u-font-size-16 u-line-height-125 "
                                                                "u-line-height-normal@mobile-max a-truncate-ellipsis "
                                                                "u-max-width-330 u-max-width-230@tablet-only")

top_100_titles = [songs.getText().strip(" \n\t") for songs in titles]
top_100_titles.insert(0, first_title.getText().strip(" \n\t"))

first_artist = soup.select_one(selector="div ul li ul li span", class_="c-label a-no-trucate a-font-primary-s "
                                                                       "lrv-u-font-size-14@mobile-max "
                                                                       "u-line-height-normal@mobile-max "
                                                                       "u-letter-spacing-0021 lrv-u-display-block "
                                                                       "a-truncate-ellipsis-2line u-max-width-330 "
                                                                       "u-max-width-230@tablet-only")
artists = soup.find_all(class_="c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max "
                               "u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block "
                               "a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only")

top_100_artists = [name.getText().strip(" \n\t") for name in artists]
top_100_artists.insert(0, first_artist.getText().strip(" \n\t"))

print(top_100_titles)
print(top_100_artists)
# idx = 0
# spotify_date = time_traveler.replace("-", "/")
# song_uri = []
# for title in top_100_titles:
#     song_search = sp.search(q=title, type="track")
#     try:  # SOLVE WHY RUFF ENDZ WONT WORK
#         for track in song_search["tracks"]["items"]:
#             print(track["album"]["artists"][0]["name"])
#             print(top_100_artists[idx])
#             if track["album"]["artists"][0]["name"].lower().split()[0] == top_100_artists[idx].lower().split()[0]:
#                 print(track["uri"])
#                 song_uri.append(track["uri"])
#                 idx += 1
#                 print(song_uri)
#                 print(idx)
#
#     except IndexError:
#         print(f"{title} doesn't exist in Spotify. Skipped.")

# playlist = sp.user_playlist_create(
#     user=user,
#     name=f"{spotify_date} --> Billboard Hot 100",
#     public=False,
#     description=f"The Top Hot 100 songs for {spotify_date}")
#
# sp.playlist_add_items(playlist_id=playlist,items=song_uri)