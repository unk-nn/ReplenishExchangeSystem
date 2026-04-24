from pathlib import Path
import json

#для коректной работы функции необходимо чтобы файл был размещен в главной папке проекта!
def get_path(folders:list, file:str):
    main_dir = Path(__file__).parent
    return main_dir.joinpath(*folders, file)
def get_json_token(json_file:str, type_token:str='access_token'):
    with open(json_file, mode='r', encoding='UTF-8') as get_token:
        json_post = json.load(get_token)
        return json_post[type_token]