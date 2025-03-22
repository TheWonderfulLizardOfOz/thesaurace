import requests
import json
import time

with open('cachedWords.json', 'r') as file:
    thesaurus = json.load(file)


def sanitiser(word):
    if not word.isalpha():
        return False
    return True

def save_thesaurus():
    with open('cachedWords.json', 'w', encoding='utf-8') as f:
        json.dump(thesaurus, f, ensure_ascii=False, indent=4)

def get_synonyms_of(word):
    if word in thesaurus.keys():
        return thesaurus[word]
    else:
        api_url = 'https://api.api-ninjas.com/v1/thesaurus?word={}'.format(word)
        response = requests.get(api_url, headers={'X-Api-Key': 'Aqv8rZ0xlEOBQjnTf4cCrw==B6zBflzo1sc2Sz6D'})
        if response.status_code == requests.codes.ok:
            sanitised = list(filter(sanitiser,response.json()["synonyms"]))
            thesaurus[word] = sanitised
            save_thesaurus()
            return thesaurus[word]
        else:
            print("Error:", response.status_code, response.text)
            return -1


word = 'foundations'
