import asyncio
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify
from AnimeParser import s
app = Flask(__name__)

baseURL = "https://nekopoi.care"

def ThreeDHentai():
  response = requests.get(f"{baseURL}/category/3d-hentai")
  html = response.text

  soup = BeautifulSoup(html, "html5lib")
  posts = soup.find('div', class_="result").parent.find_all('li')
  contents = []
  for post in posts:
    title = post.find('a').text.strip()
    url = post.find('a').attrs['href']
    descs = post.find_all('p')
    descs_ = []
    for desc in descs:
      descs_.append(desc.text.strip())
    contents.append({
      "title": title,
      "url": url,
      "description": "\n".join(descs_)
    })
  return contents

def javCosplays():
  response = requests.get(f"{baseURL}/tag/jav-cosplay")
  html = response.text

  soup = BeautifulSoup(html, "html5lib")
  posts = soup.find('div', class_="result").parent.find_all('li')
  contents = []
  for post in posts:
    title = post.find('a').text.strip()
    url = post.find('a').attrs['href']
    separators = post.find_all('p', class_="separator")
    sprts = []
    for separator in separators:
      sprts.append(separator.text.strip())
    contents.append({
      "title": title,
      "url": url,
      "detail": "\n".join(sprts)
    })
  return contents

def search(anime: str):
  try:
    loop = asyncio.new_event_loop()
    html = s(anime, loop)
    soup = BeautifulSoup(html, "html5lib")
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


def javList():
  response = requests.get(f"{baseURL}/jav-list")
  html = response.text
  soup = BeautifulSoup(html, "html5lib")

  javs = soup.find_all('div', class_="row-cells")
  
  results = []

  for jav in javs:
    if jav.text.strip() != "":
      title = jav.text
      url = jav.find('a', class_="series").attrs['href']
      seri = jav.find('a', class_="series").attrs['title'].strip()
      results.append({
        "title": title, "url": url, "seri": seri
      })
  return results

def hentaiList():
  response = requests.get(f"{baseURL}/hentai-list")
  html = response.text

  soup = BeautifulSoup(html, "html5lib")
  hentais = soup.find_all('div', class_="row-cells")
  results = []

  for hentai in hentais:
    if hentai.text.strip() != "":
      title = hentai.text
      url = hentai.find('a').attrs['href']

      # Tooltip.
      soupArea = BeautifulSoup(hentai.find('a').attrs['original-title'], "html5lib")
      image = soupArea.find('img').attrs['src']
      detail = []
      detail_p = soupArea.find_all('p')
      for detail_ in detail_p:
        detail.append(detail_.text.strip())
      results.append({
        "title": title,
        "url": url,
        "image": image,
        "detail": "\n".join(detail)
      })
  return results

@app.route("/")
def home():
  return jsonify({
    "hello": "world"
  })

@app.route("/hentai")
def hentais():
  return jsonify(hentaiList())

@app.route("/jav-cosplay")
def javCosplay():
  return jsonify(javCosplays())

@app.route("/3d-hentai")
def threedhentai():
  return jsonify(ThreeDHentai())

@app.route("/jav")
def javs():
  return jsonify(javList())

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