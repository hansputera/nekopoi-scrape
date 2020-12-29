import asyncio
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify
from AnimeParser import s
app = Flask(__name__)

baseURL = "https://nekopoi.care"


def search(anime: str):
  try:
    loop = asyncio.new_event_loop()
    html = s(anime, loop)
    soup = BeautifulSoup(html, "html5lib")
    soup = BeautifulSoup(soup.prettify(), "html5lib")
    all_contents = soup.find('div', class_="result").parent.find_all('li')
    contents = []
    for content in all_contents:
      title = content.find('h2').text.strip()
      videoURL = content.find('h2').findNext('a').attrs['href']
      thumbnail = content.find('img').attrs['src']
      description = content.find('div', class_="desc").text.strip()
      contents.append({
        "title": title,
        "url": videoURL,
        "thumbnail": thumbnail,
        "description": description.strip()
      })
    return contents
  except:
    return None
  

def newEpisodes():
  response = requests.get(baseURL)
  html = response.text

  soup = BeautifulSoup(html, "html5lib")
  allPosts = soup.find_all('div', class_="eropost")
  items = []
  for post in allPosts:
    title = post.find('h2').string.strip()
    date_ = post.find('span').string.strip()
    url = post.find('a').attrs['href']
    thumbnail = post.find('img').attrs['src']

    items.append({
      "title": title,
      "date": date_,
      "url": url,
      "thumbnail": thumbnail
    })
  return items


@app.route("/")
def home():
  return jsonify({
    "hello": "world"
  })

@app.route("/newEpisodes")
def newEpisodes_():
  episodes = newEpisodes()
  return jsonify(episodes)

@app.route("/search/<anime_name>")
def searchAnime(anime_name):
  result_anime = search(str(anime_name))
  if result_anime == None:
    return jsonify({
      "success": False,
      "message": "404 Not Found"
    })
  else:
    return jsonify({ "success": True, "result": result_anime })

if __name__ == "__main__":
  app.run(
    host="0.0.0.0",
    port=1993
  )