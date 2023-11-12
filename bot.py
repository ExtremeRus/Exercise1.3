import json
import os
from random import randrange
from urllib.request import Request, urlopen
import vk_api
from dotenv import load_dotenv
from vk_api.longpoll import VkEventType, VkLongPoll
from youtubesearchpython import VideosSearch

load_dotenv()
TOKEN = os.getenv("TOKEN")
vk_sesion = vk_api.VkApi(token=TOKEN)
longpoll = VkLongPoll(vk_sesion)
vk = vk_sesion.get_api()


def get_pokemons():
    req = Request("https://pokeapi.co/api/v2/pokemon",
                  headers={'User-Agent': 'Mozilia/5.0'})
    response = urlopen(req)
    count = json.loads(response.read())['count']

    req = Request(f"https://pokeapi.co/api/v2/pokemon/?limit={count}",
                  headers={'User-Agent': 'Mozilia/5.0'})
    response = urlopen(req)
    pokemons = json.loads(response.read())['results']
    return pokemons


def find_pokemon(name, pokemons):
    req = Request(pokemon["url"], headers={'User-Agent': 'Mozilia/5.0'})
    responce = urlopen(req)
    desc = json.loads(responce.read())
    message = f"Имя: {desc['name']}\nРост: {desc['height']}\nВес: {desc['weight']}"
    return message


def find_video(name):
    link = VideosSearch(event.text,
                        limit=1).result()['result'][0]['link']
    return link


pokemons = get_pokemons()

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        if event.from_user:
            command = event.text.split()[0].lower()
            event.text = event.text[len(command) + 1:]
            if command == "покемон":
                for pokemon in pokemons:
                    if pokemon['name'] == event.text:
                        message = find_pokemon(event.text, pokemons)
                        vk.messages.send(user_id=event.user_id, message=message, random_id=randrange(1, 1000000))
                        break
            elif command == "ютуб":
                link = find_video(event.text)
                vk.messages.send(user_id=event.user_id, message=link, random_id=randrange(1, 1000000))
