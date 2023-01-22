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

    while 1:
        #create a search request
        print("Enter the songname. If you want to exit, write '_exit': ")
        songname = input()
        if songname == '_exit':
            break
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

        #save searched songs as a dict format
        print(f'Responses for request "{songname}: "')
        songs = []; i = 0
        for name in songs_meta:
            id = name['id'].split('-')[2]
            url = 'https://ru.hitmotop.com/song/' + id
            html_page_song = request("GET", url=url).text
            soup1 = BeautifulSoup(html_page_song, 'lxml')
            download_link = 'https:' + soup1.find('div', class_='p-track-download').find('a').get('href')
            songs.append({})
            songs[i] = {'songname' : name['artist'] + ' - ' + name['title'] , 'url' : download_link}
            print(f'{i + 1} : {songs[i]}')
            i += 1

        while 1:
            #choice of the song what you need
            print('Enter the number of your wish song: ')
            num = input()
            if num == '_new':
                break
            for_download = songs[int(num) - 1]

            #download the chosen track
            os.chdir(folder)
            download = request('GET', url=for_download['url'])
            if download.status_code == 200:
                with open(for_download['songname'] + '.mp3', 'wb') as file:
                    file.write(download.content)
                    print("The song has been download successfully...")
            print('You can choose one more song. In order to make new request write _new')


if __name__ == '__main__':
    main()