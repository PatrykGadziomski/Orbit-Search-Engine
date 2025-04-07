import requests

url = "https://ntrs.nasa.gov/api/citations/search"

params = {
    "q": "mission report",
    "pageSize": 100,
    "start": 0,
    "sortBy": "publicationDate",
    "order": "desc"
}

response = requests.get(url, params=params)
data = response.json()

print(len(data['results']))
# for doc in data['results']:
#     print(doc['title'])
#     print(doc['downloads'][0]['links']['fulltext'])
#     break