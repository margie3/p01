import json
import requests

ending = False
win = False

url = "https://coin-flip1.p.rapidapi.com/headstails"

headers = {
	"x-rapidapi-key": "bc3743a599msh4774854b06469a0p15e76ejsnaf4ebd77d8cf",
	"x-rapidapi-host": "coin-flip1.p.rapidapi.com"
}

response = requests.get(url, headers=headers)
result = response.json().get("outcome")

def flip(guess):
    global ending, win, result
    response = requests.get(url, headers=headers)
    result = response.json().get("outcome")
    ending = False
    win = False
    if result == guess:
        ending = True
        win = True
    else:
        ending = True
        win = False