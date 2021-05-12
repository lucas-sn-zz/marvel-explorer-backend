from dotenv import load_dotenv
import hashlib
import os
import requests

marvel_url_prefix = 'https://gateway.marvel.com:443/v1/public'

load_dotenv()


def hash_generate():
    m = hashlib.md5()
    hash_value = f"{os.getenv('MARVEL_CONST')}{os.getenv('MARVEL_PRIVATE_KEY')}{os.getenv('MARVEL_PUBLIC_KEY')}"
    return {'ts': os.getenv('MARVEL_CONST'), 'apikey': os.getenv('MARVEL_PUBLIC_KEY'), 'hash': hashlib.md5(str.encode(hash_value)).hexdigest()}


class MarvelModel:
    @ staticmethod
    def get_characters_by_name(character_name, page):
        offset = (1 - page) * 20
        if character_name == None:
            request_values = requests.get(
                url=f"{marvel_url_prefix}/characters", params={"offset": offset, **hash_generate(), }).json()
        else:
            request_values = requests.get(
                url=f"{marvel_url_prefix}/characters", params={"offset": offset, **hash_generate(), 'nameStartsWith': character_name}).json()
        data = {
            "current_page": page,
            "count": 20,
            "pages": round(request_values['data']['total'] + 0.5),
            "results": {int(character['id']): character for character in request_values['data']['results']}
        }
        return data

    def get_character_details(id_character):
        request_values = requests.get(
            url=f"{marvel_url_prefix}/characters/{id_character}", params={**hash_generate()}).json()
        data = {
            "results": {result["id"]: result for result in request_values['data']["results"]}
        }
        return data

    def get_comic_details(id_comic):
        request_values = requests.get(
            url=f"{marvel_url_prefix}/comics/{id_comic}", params={**hash_generate()}).json()
        data = {
            "results": {result["id"]: result for result in request_values['data']["results"]}
        }
        return data

    def get_comics_by_name(name, page):
        offset = (page - 1) * 20
        if name == None:
            request_values = requests.get(
                url=f"{marvel_url_prefix}/comics", params={"offset": offset, **hash_generate(), }).json()
        else:
            request_values = requests.get(
                url=f"{marvel_url_prefix}/comics", params={"offset": offset, **hash_generate(),
                                                           'titleStartsWith': name}).json()
        data = {
            "current_page": page,
            "count": 20,
            "pages": round(request_values['data']['total'] + 0.5),
            "results": {int(comic['id']): comic for comic in request_values['data']['results']} if len(request_values['data']['results']) > 0 else []
        }
        return data
