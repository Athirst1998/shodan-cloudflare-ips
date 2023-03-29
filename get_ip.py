import requests
import bs4
from bs4 import BeautifulSoup
import re

data = requests.get("https://www.shodan.io/search?query=cloudflare")

soup = BeautifulSoup(data.text, features="html.parser")
results = soup.find_all("div", {"class": "result"})
page_number = 0

for result in results:

    check_cdn: bs4.element.Tag = result.find("a", {"class": "tag"})
    if check_cdn.text == 'cdn':
        print('=' * 30)
        title = (result.find("a", {"class": "title text-dark"}))
        print(f"title: {title.text.strip()}")
        ssl = result.find("strong")
        ssl_text = re.findall(r'>(.+)</', str(ssl))
        ssl_text = "none" if not ssl_text else ssl_text[0]
        print(f"ssl: {ssl_text.strip()}")
        location = result.find("img", {"class": "flag"})
        location_text = re.findall(r'title="(.+)"\s', str(location))
        location_text = None if not location_text else location_text[0]
        print(f"location: {location_text.strip()}")
        host_names = result.find_all("li", {"class": "hostnames text-secondary"})
        print('host names:')
        for name in host_names:
            if name.text != "sni.cloudflaressl.com":
                print(f"    {name.text.strip()}")
