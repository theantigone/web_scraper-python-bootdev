import requests
from bs4 import BeautifulSoup

# 1. Fetch the webpage
url = "https://www.iana.org/help/example-domains"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# 2. Find all <img> tags
images = soup.find_all("img")
print("lol")
print(images)

# 3. Extract the 'src' from each tag
for img in images:
    img_url = img.get("src")
    print("hi")
    print(img_url)
