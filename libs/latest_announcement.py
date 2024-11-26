import requests
from bs4 import BeautifulSoup

URL = "https://alumnos.ibeltran.com.ar"

def fetch_latest_announcement():
    global last_seen
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    latest_announcement = soup.select_one(".noticia h3").text.strip()

    if latest_announcement:
        last_seen = latest_announcement
        print("New announcement:", latest_announcement)
        return latest_announcement