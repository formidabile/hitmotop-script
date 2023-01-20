from requests import request
from bs4 import BeautifulSoup
import lxml
import os
import ast

def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_id(id):
    return id.split('-')[2]

def main():
    #create directory with music if it is necessary
    folder = 'D:\музыка'
    create_dir(folder)

    #create a search request
    songname = input()
    url = f'https://ru.hitmotop.com/search?q={songname.replace(" ", "+")}'
    html_page = request('GET', url=url).text
    #with open('html_page.html', 'w', encoding='utf-8') as file:
    #    file.write(html_page)

    #parse the request
    soup = BeautifulSoup(html_page, 'lxml')
    list_of_songs = soup.find_all('li', class_='tracks__item track mustoggler')
    songs_meta = []
    for song_info in list_of_songs:
        songs_meta.append(ast.literal_eval(song_info.get('data-musmeta')))

    #save searches songs as a dict format
    songs = []; i = 0
    for name in songs_meta:
        id = name['id'].split('-')[2]
        songs.append({})
        songs[i] = {'songname' : name['artist'] + ' - ' + name['title'] , 'url' : 'https://ru.hitmotop.com/song/' + id}
        print(f'{i + 1} : {songs[i]}')
        i += 1

    #choice of the song what you need
    num = int(input())
    for_download = songs[num - 1]
    html_page_song = request('GET', url=for_download['url']).text
    soup1 = BeautifulSoup(html_page_song, 'lxml')
    download_link = 'https:' + soup1.find('div', class_='p-track-download').find('a').get('href')

    #download the chosen track
    os.chdir(folder)
    download = request('GET', url=download_link)
    if download.status_code == 200:
        with open(for_download['songname'] + '.mp3', 'wb') as file:
            file.write(download.content)
            print("The song has been download successfully...")


if __name__ == '__main__':
    main()