import json
import requests

end = False
win = False

response = requests.get("https://rpg-dice-roller-api.djpeacher.com/api/roll/2d6")
num = response.json().get("total")

def guess(userguess):
    global end, win, num
    end = False
    win = False
    if userguess == num:
        end = True
        win = True
    else:
        end = True
        win = False