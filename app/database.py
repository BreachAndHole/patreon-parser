import json
import os

from app.parsedpostdata import ParsedPostData
from app import config


def __convert_post_data_to_dict(parsed_post_data: ParsedPostData) -> dict:
    return {
        'id': parsed_post_data.id,
        'title': parsed_post_data.title,
        'url': parsed_post_data.url,
        'youtube_url': parsed_post_data.youtube_url,
    }


def __prepare_posts_to_dump(posts_data: list[ParsedPostData]) -> list[dict]:
    json_data = []
    for post in posts_data:
        json_data.append(__convert_post_data_to_dict(post))
    return json_data


def get_data_from_json(file_name=config.JSON_DB_FILENAME) -> list[dict]:
    if not os.path.exists(file_name):
        return []

    with open(file_name, 'r', encoding='utf-8') as fin:
        file_json: list[dict] = json.load(fin)
    return file_json


def save_data_to_json(posts_data: list[ParsedPostData], file_name=config.JSON_DB_FILENAME) -> None:
    json_data = __prepare_posts_to_dump(posts_data)

    if not os.path.exists(file_name):
        with open(file_name, 'w', encoding='utf-8') as fout:
            json.dump(json_data, fout, indent=4)
        return

    file_json = get_data_from_json(file_name)

    for data in json_data:
        file_json.append(data)

    with open(file_name, 'w', encoding='utf-8') as fout:
        json.dump(file_json, fout, indent=4)


if __name__ == '__main__':
    post_1 = ParsedPostData(
        id=1,
        title='123123',
        url='123123',
        youtube_url='123123'
    )
    post_2 = ParsedPostData(
        id=2,
        title='aisujdgbh',
        url='aisujdgbh',
        youtube_url='aisujdgbh'
    )
    # posts = [post_1, post_2]
    #
    # update_json(posts)
