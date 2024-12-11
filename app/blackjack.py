import requests
import json
import __init__

def run():
    response = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1")    
    print(response)
