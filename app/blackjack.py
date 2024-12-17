import json
import requests

win = False
end = False
bust = False
yourturn = False
usercards = 2
dealercards = 2
response = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=6") 
deckid = response.json().get("deck_id")
user = 0
dealer = 0
user_imgs = {}
dealer_imgs = {}

def setup():
    global win, end, bust, yourturn, usercards, dealercards, deckid, user, dealer, user_imgs, dealer_imgs
    draw = requests.get("https://deckofcardsapi.com/api/deck/" + deckid + "/draw/?count=4")
#     print(draw.json().get("cards"))
    user_imgs = {}; dealer_imgs = {}; win = False; end = False; bust = False; usercards = 2; dealerscards = 2
    user_imgs[0] = draw.json().get("cards")[0].get("image"); dealer_imgs[0] = draw.json().get("cards")[1].get("image") #first card to user, second to dealer
    user_imgs[1] = draw.json().get("cards")[2].get("image"); dealer_imgs[1] = draw.json().get("cards")[3].get("image") #storing drawn card images for html, dcard2 not shown
    print(user_imgs[0])
#     print(draw.json().get("deck_id"))
#     print(draw.json().get("cards")[0].get("value"))
    u1 = draw.json().get("cards")[0].get("value"); d1 = draw.json().get("cards")[1].get("value")
    u2 = draw.json().get("cards")[2].get("value"); d2 = draw.json().get("cards")[3].get("value")
    u1 = convert(u1); u2 = convert(u2); d1 = convert(d1); d2 = convert(d2)
    user = int(u1) + int(u2)
    dealer = int(d1) + int(d2)
#     print(value1)
#     print(value2)
    over()
    yourturn = True

def hit():
    global win, end, bust, yourturn, usercards, dealercards, deckid, user, dealer, user_imgs, dealer_imgs
    hit = requests.get(f"https://deckofcardsapi.com/api/deck/{deckid}/draw/?count=1")
    hitimg = hit.json().get("cards")[0].get("image")
    hitcard = hit.json().get("cards")[0].get("value")
    if (yourturn):
        user_imgs[usercards] = hitimg
        usercards = usercards + 1
        user = user + convert(hitcard)
    else:
        dealer_imgs[dealercards] = hitimg
        dealercards = dealercards + 1
        dealer = dealer + convert(hitcard)
    over()
    yourturn = not yourturn

def stay():
    global win, end, bust, yourturn, usercards, dealercards, deckid, user, dealer, user_imgs, dealer_imgs
    if dealer < 17 and yourturn == False:
        hit()
    else:
        if user > dealer:
            win = True
        else:
            win = False
        end = True

def over():
    global win, end, bust, yourturn, usercards, dealercards, deckid, user, dealer, user_imgs, dealer_imgs
    if user == 21:
        win = True
        end = True
    elif dealer == 21:
        win = False
        end = True
    elif user > 21:
        win = False
        bust = True
        end = True
    elif dealer > 21:
        win = True
        bust = True
        end = True

def bot():
    global win, end, bust, yourturn, usercards, dealercards, deckid, user, dealer, user_imgs, dealer_imgs
    if (not yourturn):
        if dealer < 17:
            hit()
        else:
            stay()

def convert(value):
    if value in ["KING", "QUEEN", "JACK"]:
        return 10
    if value == "ACE":
        return 11
    return int(value)

