import requests
import json
with open('cachedWords.json', 'r') as file:
    thesaurus = json.load(file)

word = 'foundations'
api_url = 'https://api.api-ninjas.com/v1/thesaurus?word={}'.format(word)
response = requests.get(api_url, headers={'X-Api-Key': 'Aqv8rZ0xlEOBQjnTf4cCrw==B6zBflzo1sc2Sz6D'})
if response.status_code == requests.codes.ok:
    print(response.text)
    print(response.json()["synonyms"])
    thesaurus[word] = response.json()["synonyms"]
else:
    print("Error:", response.status_code, response.text)

with open('cachedWords.json', 'w', encoding='utf-8') as f:
    json.dump(thesaurus, f, ensure_ascii=False, indent=4)


