import httpx
import pandas as pd


def google_search(query, exactTerms,**params):
    base_url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'key': "AIzaSyD944DvcguV7AW7dz-kTZL3kuwSPB8Zipg",
        'cx': "720afaae479f04ee9",
        'q': query,
        'exactTerms': exactTerms,
        **params        
    }
    response = httpx.get(base_url, params=params)
    response.raise_for_status()
    return response.json()

search_results = []
for i in range(1, 100, 10):
    response = google_search('fonte 120 jfa',"120", start=i)
    search_results.extend(response.get('items', []))


for i in search_results:
    print(i['title'])
    print(i['link'])