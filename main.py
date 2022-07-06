import requests
from bs4 import BeautifulSoup

f = open("main.html", "w+")
html_str = """<!DOCTYPE html>
<html lang="en">

    <head>

        <title>Anime Info</title>

    </head>

    <body>
    
        <center>

            <h1>Anime Info</h1>
            
            <table style="width:100%">
                
                <tr>
                    
                    <th><u>Image</u></th>
                    <th><u>Title</u></th>
                    <th><u>English Title</u></th>
                    <th><u>Description</u></th>
                    <th><u>Rating</u></th>
                    <th><u>Genres</u></th>
                    
                </tr>
"""
f.write(html_str)
f.close()

print("Please type each anime title on a new line and say \"Done\" when you are finished")
animes = []
while True:
    answer = input(" ")
    if answer == "Done":
        break
    else:
        animes.append(answer)

# animes = ["Samurai Champloo", "Toradora"]

for show in animes:

    item_url = show.replace(" ", "%20")

    url = "https://myanimelist.net/anime.php?q=" + item_url

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    result = soup.find(class_='hoverinfo_trigger fw-b fl-l')
    result_link = result['href']

    url = result_link

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    name = str(soup.find("span", itemprop="name"))
    image_url = str(soup.find("img", itemprop="image"))
    description = str(soup.find("span", itemprop="description")).replace("[Written by MAL Rewrite]", "")
    score = str(soup.find("span", itemprop="ratingValue"))

    rating = str(soup.find(text="Rating:").parent.parent).replace("Rating:", "")
    eng_name = str(soup.find(text="English:").parent.parent).replace("English:", "")
    duration = str(soup.find(text="Duration:").parent.parent).replace("Duration:", "")
    genres = str(soup.find(text="Genres:").parent.parent.text).replace("Genres:", "")
    status = str(soup.find(text="Status:").parent.parent).replace("Status:", "")
    episode_num = str(soup.find(text="Episodes:").parent.parent).replace("Episodes:", "")
    premiere_date = str(soup.find(text="Premiered:").parent.parent).replace("Premiered:", "")

    anime_info = [name, eng_name, description, score, rating, duration, episode_num, genres, status, premiere_date, image_url]

    fmt = "<th>{}</th>"
    with open('main.html', 'a') as fd:
        fd.write("<tr>")
        fd.write(fmt.format(image_url))
        fd.write(fmt.format(name))
        fd.write(fmt.format(eng_name))
        fd.write(fmt.format(description))
        fd.write(fmt.format(rating))
        fd.write(fmt.format(genres))
        fd.write("</tr>")


f = open("main.html", "a")
html_str = """
            </table>
            
        </center>
        
    </body>

</html>
"""
f.write(html_str)
f.close()
