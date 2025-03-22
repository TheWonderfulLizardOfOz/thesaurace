import requests
import json
import random

with open('cachedWords.json', 'r') as file:
    thesaurus = json.load(file)

def get_all_words():
    return list(thesaurus.keys())

def sanitiser(word):
    for letter in word:
        if letter not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
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
            sanitised = sorted(list(set(filter(sanitiser,response.json()["synonyms"]))))
            thesaurus[word] = sanitised
            save_thesaurus()
            return thesaurus[word]
        else:
            print("Error:", response.status_code, response.text)
            return -1
    
def get_scrabble_score_of(word):
    score = 0
    for letter in word:
        if letter in "aeiounrtls":
            score += 1
        elif letter in "dg":
            score += 2
        elif letter in "bcmp":
            score += 3
        elif letter in "fhvwy":
            score += 4
        elif letter in "k":
            score += 5
        elif letter in "jx":
            score += 8
        elif letter in "qz":
            score += 10
    return score

def sanitise_thesaurus():
    clean_thesaurus = {}
    for word in thesaurus.keys():
        clean_thesaurus[word] = sorted(list(set(filter(sanitiser,thesaurus[word]))))
    with open('cachedWords.json', 'w', encoding='utf-8') as f:
        json.dump(clean_thesaurus, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    play = input("Play game? Y/N")
    if play == "Y":
        destination = "building"
        searchHistory = []
        for i in range(15):
            synonyms = get_synonyms_of(destination)
            if len(synonyms) > 0:
                searchHistory.append(destination)
                destination = random.choice(synonyms)
            else:
                destination = searchHistory[-1]
                searchHistory = searchHistory[:-1]
        word = "foundations"
        round = 0
        history = []
        while word != destination:
            print(f"DESTINATION: {destination}")
            print(f"CURRENT WORD: {word}")
            synonyms = get_synonyms_of(word)
            for index, synonym in enumerate(synonyms):
                print(f"{index}: {synonym}")
            if len(history) > 0:
                print(f"UNDO: {history[-1]}")
                choice = input("Select choice index or UNDO: ")
            else:
                choice = input("Select choice: ")
            if choice == "UNDO":
                word = history[-1]
                history = history[:-1]
            else:
                history.append(word)
                word = synonyms[int(choice)]
                
            
        