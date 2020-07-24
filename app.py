import logging

from flask import Flask, request
from config import VERIFY_TOKEN

from messenger import get_message, RandomAnimeBot
from error import InvalidMethodError


app = Flask(__name__)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@app.route('/', methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        token_sent = request.args.get('hub.verify_token')

        return verify_fb_token(token_sent)

    elif request.method == 'POST':
        output = request.get_json()

        for event in output['entry']:
            messaging = event['messaging']

            for message in messaging:

                if message.get('message'):
                    recipient_id = message['sender']['id']
                    response, img_url = get_message()

                    chatbot = RandomAnimeBot(recipient_id, response, img_url)
                    bot_message = chatbot.send_message()

        return 'message processed'

    else:
        raise InvalidMethodError('invalid choice of API method')


def verify_fb_token(tokenSent):
    if tokenSent == VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    else:
        return 'invalid verification token'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
