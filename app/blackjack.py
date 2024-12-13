import json
import requests

win = False
end = False
yourturn = False
response = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=6") 
#     data = response.text
#     print(data)
deckid = response.json().get("deck_id")
user = 0
dealer = 0

def setup():
    draw = requests.get("https://deckofcardsapi.com/api/deck/" + deckid + "/draw/?count=4")
#     print(draw.json().get("cards"))
    uimg1 = draw.json().get("cards")[0].get("image"); dimg1 = draw.json().get("cards")[1].get("image") #first card to user, second to dealer
    uimg2 = draw.json().get("cards")[2].get("image"); dimg2 = draw.json().get("cards")[3].get("image") #storing drawn card images for html, dcard2 not shown
#     print(draw.json().get("deck_id"))
#     print(draw.json().get("cards")[0].get("value"))
    u1 = draw.json().get("cards")[0].get("value"); d1 = draw.json().get("cards")[1].get("value")
    u2 = draw.json().get("cards")[2].get("value"); d2 = draw.json().get("cards")[3].get("value")
    u1 = convert(u1); u2 = convert(u2); d1 = convert(d1); d2 = convert(d2)
    user = int(u1) + int(u2)
    dealer = int(d1) + int(d2)
#     print(value1)
#     print(value2)
    end()
    yourturn = True

def hit():
    hit = requests.get("https://deckofcardsapi.com/api/deck/" + deckid + "/draw/?count=1")
    hitimg = hit.json().get("cards")[0].get("image")
    end()
    yourturn = not yourturn

def stay():
    if (user > dealer):
        win = True
        end = True
    else:
        win = False
        end = True
    yourturn = not yourturn

def end():
    if (user == 21):
        print("you win")
        win21 = True
        end = True
    if (dealer == 21):
        print("you lose")
        lose21 = True
        end = True
    if (user > 21):
        print("you lose")
        userbust = True
        end = True
    if (dealer > 21):
        print("you win")
        dealerbust = True
        end = True

def convert(value):
    if (value == "KING" or value == "QUEEN" or value == "JACK"):
        value = 10
    if (value == "ACE"):
        value = 11
    return value

setup()
hit()
