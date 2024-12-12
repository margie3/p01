import json
import requests

def setup():
    response = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=6") 
    data = response.text
#     print(data)
    deckid = (response.json().get("deck_id"))
    draw = requests.get("https://deckofcardsapi.com/api/deck/" + deckid + "/draw/?count=2")
#     print(draw.json().get("cards"))
    card1 = draw.json().get("cards")[0].get("image")
    card2 = draw.json().get("cards")[1].get("image") #storing drawn card images for html
#     print(draw.json().get("deck_id"))
setup()