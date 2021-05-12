from models.character import CharacterModel
from models.comic import ComicModel
from models.marvel import MarvelModel


class UserCharacterServices:
    @staticmethod
    def get_user_characters_details(id_user, name, **kwargs):
        ids_user_characters = CharacterModel.find_user_characters(
            id_user, name)
        result_dict = {}
        for key in ids_user_characters:
            result_dict[key] = {'is_favorite': True}
            result_dict[key].update(MarvelModel.get_characters_details(
                id_character=key)["results"][key])
        return result_dict


class MarvelCharacterServices:
    @staticmethod
    def get_marvel_characters(id_user, page=1, character_name=None):
        characters = MarvelModel.get_characters_by_name(
            page=page, character_name=character_name)
        try:
            user_characters = CharacterModel.find_user_characters_by_ids(
                id_user, list(characters['results'].keys()))
            for key in characters['results']:
                if key in user_characters:
                    characters['results'][key]['is_favorite'] = True
                else:
                    characters['results'][key]['is_favorite'] = False
            return(characters), 200
        except Exception as e:
            return {"msg": "An error has occurred ",
                    "error": str(e)}, 500


class MarvelCharacterDetailsServices:
    @staticmethod
    def get_marvel_character_details(id_user, id_character):
        character = MarvelModel.get_character_details(id_character)
        user_character = CharacterModel.find_by_id(id_user, id_character)
        character['results'][id_character]['is_favorite'] = True if user_character != None else False
        for item in range(len(character['results'][id_character]['comics']['items'])):
            character['results'][id_character]['comics']['items'][item]['id'] = int(
                character['results'][id_character]['comics']['items'][item]['resourceURI'].split('/')[-1])
            character['results'][id_character]['comics']['items'][item]['is_favorite'] = True if ComicModel.find_by_id(
                id_user, character['results'][id_character]['comics']['items'][item]['id']) != None else False
        return character
