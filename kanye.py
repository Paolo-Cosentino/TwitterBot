import requests
import json


def get_new_quote():
    return '"{}" -Kanye West'.format(json.loads(requests.get('https://api.kanye.rest').text)['quote'])
