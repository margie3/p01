import json
import requests

win = False
end = False
yourturn = False
response = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=6") 
deckid = response.json().get("deck_id")
user = 0
dealer = 0

def setup():
    global user, dealer, yourturn  # Add global to modify the game state

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

    return {"user_score": user, "dealer_score": dealer, "user_images": [uimg1, uimg2], "dealer_images": [dimg1, dimg2]}

def hit():
    global user, yourturn

    hit = requests.get(f"https://deckofcardsapi.com/api/deck/{deckid}/draw/?count=1")
    hitimg = hit.json().get("cards")[0].get("image")
    user_card = hit.json().get("cards")[0].get("value")

    user += convert(user_card)
    yourturn = not yourturn

    return {"user_score": user, "user_image": hitimg}

def stay():
    global user, dealer, win, end, yourturn

    if user > dealer:
        win = True
    else:
        win = False
    end = True
    yourturn = not yourturn

    return {"game_over": True, "win": win, "user_score": user, "dealer_score": dealer}

def end():
    global win, end

    if user == 21:
        win = True
        end = True
    elif dealer == 21:
        win = False
        end = True
    elif user > 21:
        win = False
        end = True
    elif dealer > 21:
        win = True
        end = True

def convert(value):
    if value in ["KING", "QUEEN", "JACK"]:
        return 10
    if value == "ACE":
        return 11
    return int(value)

