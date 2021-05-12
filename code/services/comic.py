from models.comic import ComicModel
from models.character import CharacterModel
from models.marvel import MarvelModel

class UserComicServices:
    @staticmethod
    def get_user_comics_details(id_user,name):
        ids_user_comics = ComicModel.find_user_comics(id_user,name)
        result_dict = {'results':{}}
        for key in ids_user_comics:
            result_dict['results'][key] = {'is_favorite': True}
            result_dict['results'][key].update(MarvelModel.get_comic_details(id_comic=key)["results"][key])
            for item in range(len(result_dict['results'][key]['characters']['items'])):
                result_dict['results'][key]['characters']['items'][item]['id'] = int(result_dict['results'][key]['characters']['items'][item]['resourceURI'].split('/')[-1])
                result_dict['results'][key]['characters']['items'][item]['is_favorite'] = True if CharacterModel.find_by_id(id_user, result_dict['results'][key]['characters']['items'][item]['id']) != None else False
        return result_dict

class MarvelComicServices:
    @staticmethod
    def get_marvel_comics(id_user,page, name):
        comics = MarvelModel.get_comics_by_name(page=page,name=name)
        user_comics = ComicModel.find_user_comics_by_ids(id_user,list(comics['results'].keys()))
        for key in comics['results']:
            if key in user_comics:
                comics['results'][key]['is_favorite'] = True
            else:
                comics['results'][key]['is_favorite'] = False
            for item in range(len(comics['results'][key]['characters']['items'])):
                comics['results'][key]['characters']['items'][item]['id'] = int(comics['results'][key]['characters']['items'][item]['resourceURI'].split('/')[-1])
                comics['results'][key]['characters']['items'][item]['is_favorite'] = True if CharacterModel.find_by_id(id_user, comics['results'][key]['characters']['items'][item]['id']) != None else False
        return(comics)

class MarvelComicDetailsServices:
    @staticmethod
    def get_marvel_comic_details(id_user,id_comic):
        comics = MarvelModel.get_comic_details(id_comic)
        user_comics = ComicModel.find_by_id(id_user, id_comic)
        comics['results'][id_comic]['is_favorite'] = True if user_comics != None else False
        for item in range(len(comics['results'][id_comic]['characters']['items'])):
            comics['results'][id_comic]['characters']['items'][item]['id'] = int(comics['results'][id_comic]['characters']['items'][item]['resourceURI'].split('/')[-1])
            comics['results'][id_comic]['characters']['items'][item]['is_favorite'] = True if CharacterModel.find_by_id(id_user, comics['results'][id_comic]['characters']['items'][item]['id']) != None else False
        return comics
