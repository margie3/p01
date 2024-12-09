import urllib
import urllib.request
import json

def blackjack():
    uResp = urllib.request.urlopen("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=6")
#     info = uResp.read()
#     load = json.loads(info)
#     print(json.dumps(load))
    print("You Won!")

blackjack()
