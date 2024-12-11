import json
import requests

def run():
    response = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=6")
    print(response.text)
    data = response.text
    deckid = data[30:42]
    print(deckid)
    draw = requests.get("https://deckofcardsapi.com/api/deck/" + deckid + "/draw/?count=2")
    print(draw)
    print(draw.text)
run()