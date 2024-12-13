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
#     print(draw.json().get("cards")[0].get("value"))
    value1 = draw.json().get("cards")[0].get("value")
    value2 = draw.json().get("cards")[1].get("value")
    if (value1 == "KING" or value1 == "QUEEN" or value1 == "JACK"):
        value1 = 10
    if (value1 == "ACE"):
        value1 = 11
    if (value2 == "KING" or value2 == "QUEEN" or value2 == "JACK"):
        value2 = 10
    if (value2 == "ACE"):
        value2 = 11
    print(value1)
    print(value2)
    if ((int)(value1) + (int)(value2) == 21):
        print("you win")
    print((int)(value1) + (int)(value2)) 
    print((int)(value1) + (int)(value2) == 21)
setup()