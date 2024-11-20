import requests

input = input("Buscar por vídeos: ")

prompt = input.replace(" ", "+")

url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&key=AIzaSyCyxXROEnVVLLSRmb04or9-JsxJsJ9ZDt4&maxResults=3&q={prompt}"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

data = response.json()

links = []

for item in data['items']:
    links.append(f"https://www.youtube.com/watch?v={item['id']['videoId']}")

print(links)

