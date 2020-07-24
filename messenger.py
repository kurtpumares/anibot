from random import choice

from config import ACCESS_TOKEN
from pymessenger.bot import Bot
from jikanpy import Jikan


MAX_GENRE_COUNT = 43


def get_message():
    meta = get_random_from_100()

    title = meta['title']
    genres = meta['genres']
    image_url = meta['image_url']

    message = f'Title: {title}\nGenres: {', '.join(genres)}'

    return message, image_url


def get_random_from_100():
    jikan = Jikan()

    result = jikan.genre(type='anime', genre_id=choice(range(MAX_GENRE_COUNT)))
    anime_meta = result['anime'][choice(range(99))]
    genres = []

    for i in range(len(anime_meta['genres'])):
        genres.append(anime_meta['genres'][i]['name'])

    meta_data = dict(title=anime_meta['title'], genres=genres,
                     mal_id=anime_meta['mal_id'], url=anime_meta['url'],
                     synopsis=anime_meta['synopsis'],
                     image_url=anime_meta['image_url'],
                     score=anime_meta['score'], type=anime_meta['type'],
                     airing_start=anime_meta['airing_start'])

    return meta_data


class RandomAnimeBot:

    def __init__(self, recipientID, response, imageURL=None):
        self.recipientID = recipientID
        self.response = response
        self.imageURL = imageURL

    def send_message(self):
        bot = Bot(ACCESS_TOKEN)

        if self.imageURL:
            bot.send_image_url(self.recipientID, self.imageURL)

        bot.send_text_message(self.recipientID, self.response)

        return 'success'
