from azapi import AZlyrics
import pprint
import re
import os 

api = AZlyrics()

data_directory = "./"
grabbed_songs = []
print("grabbing songs already collected...")
for filename in os.listdir(data_directory):
    end = re.search("-", filename)
    if end is not None:
        end = end.start()
        filename = filename[:end].strip().lower()
        grabbed_songs.append(filename)

songs = api.getSongs('J Cole')

uncollected_total = 0
for song in songs.keys():
    pprint.pprint("Collecting: "+song, indent=4)
    if song.lower() not in grabbed_songs:
        try:
            lyric = api.getLyrics(artist='J Cole'.lower(), title=song.lower())
        except Exception as e:
            print(e)
            print(f"COUND NOT RETRIEVE {song}")
            uncollected_total += 1
    else:
        print(f"already grabbed {song}")

print("Uncollected total:", uncollected_total)

# OLD SCRAPER // THANK YOU github:elmoiv
# import requests 
# from bs4 import BeautifulSoup
# import os
# import time

# main_url = "https://www.azlyrics.com/j/jcole.html"
# base_url = "https://www.azlyrics.com"

# main_page = requests.get(main_url)
# main_soup = BeautifulSoup(main_page.text, "lxml")

# album_list = main_soup.find(id="listAlbum")

# song_list = album_list.find_all("div", {"class": "listalbum-item"})

# for song in song_list:
#     time.sleep(10)
#     link = base_url + song.find("a")['href'][2:]    
#     curr_song_page = requests.get(link)
#     curr_soup = BeautifulSoup(curr_song_page.text, "lxml")
#     song_title = curr_soup.find_all("b")[1]
#     song_html = song_title.next_element.next_element.next_element.next_element.next_element
#     # first removing all <br/>
#     for e in song_html.findAll('br'):
#         e.extract()
#     for e in song_html.findAll('i'):
#         e.extract()
#     lines = []
#     for elem in song_html:
#         if elem == None:
#             continue
#         else:
#             try:
#                 lines.append(elem.replace("\n", "").replace("\r", "").strip())
#             except Exception as e:
#                 print("trouble element:")
#                 print(elem)
#                 break
#     lines = lines[2:]
#     if len(lines) > 10:
#         print("Adding " + song_title.string)
#         print("# lines:", len(lines))
#         with open("data/"+song_title.string.replace(" ", "-").strip('"'), "w") as f:
#             for line in lines:
#                 f.write(line)
#                 f.write("\n")
#     else:
#         print("Problem CHILD")
#         print(song_title.string)
#         print(lines)
#         song_html = song_title.next_element.next_element.next_element.next_element
#         for elem in song_html:
#             print(elem)
