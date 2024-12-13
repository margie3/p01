import json
import requests

def setup():
    response = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=6") 
    data = response.text
#     print(data)
    deckid = (response.json().get("deck_id"))
    draw = requests.get("https://deckofcardsapi.com/api/deck/" + deckid + "/draw/?count=4")
#     print(draw.json().get("cards"))
    u1 = draw.json().get("cards")[0].get("image") #first card to user, second to dealer
    d1 = draw.json().get("cards")[1].get("image")
    u2 = draw.json().get("cards")[2].get("image")
    d2 = draw.json().get("cards")[3].get("image") #storing drawn card images for html, dcard2 not shown
#     print(draw.json().get("deck_id"))
#     print(draw.json().get("cards")[0].get("value"))
    u1 = draw.json().get("cards")[0].get("value")
    d1 = draw.json().get("cards")[0].get("value")
    u2 = draw.json().get("cards")[1].get("value")
    d2 = draw.json().get("cards")[0].get("value")
    u1 = convert(u1)
    u2 = convert(u2)
    d1 = convert(d1)
    d2 = convert(d2)
#     print(value1)
#     print(value2)
    if ((int)(u1) + (int)(u2) == 21):
        print("you win")
        return True
    if ((int)(d1) + (int)(d2) == 21):
        print("you lose")
        return True
    return False
    
def hit():
    hit = requests.get("https://deckofcardsapi.com/api/deck/" + deckid + "/draw/?count=1")
    
def convert(value):
    if (value == "KING" or value == "QUEEN" or value == "JACK"):
        value = 10
    if (value == "ACE"):
        value = 11
    return value

setup()