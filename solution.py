import requests
import json
import re
import datetime

API_ACCESS_TOKEN = '17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711'
API_VERSION = 5.71
API_URL = 'https://api.vk.com/method/'


class VKAPI(object):
    def __init__(self, api_url=API_URL, version=API_VERSION,
                 access_token=API_ACCESS_TOKEN):
        self.access_token = access_token
        self.version = version
        self.api_url = api_url
        self.user_id = 0
        self.user_friends = list()

    def __add_data(self, data):
        data['access_token'] = self.access_token
        data['v'] = self.version
        return data

    def get(self, method_name, data):
        url = self.api_url + method_name
        try:
            r = requests.get(url, params=self.__add_data(data))
        except IOError:
            return dict(response=list(), is_error=True)
        answ = r.json()
        answ.update({'is_error': False})
        return answ

    def post(self, method_name, data):
        url = self.api_url + method_name
        data['access_token'] = self.access_token
        data['v'] = self.version
        try:
            r = requests.post(url, data=json.dumps(self.__add_data(data)))
        except IOError:
            return dict(response=list(), is_error=True)
        answ = r.json()
        answ.update({'is_error': False})
        return answ


class VKUser(VKAPI):
    def __init__(self, uid):
        super().__init__()
        self.uid = uid

    def get_user(self):
        data = dict(user_ids=self.uid)
        user_data = self.get(method_name='users.get', data=data)
        if user_data['is_error']:
            return self.user_id

        if 'response' in user_data.keys() and len(user_data['response']) == 1:
            self.user_id = user_data['response'][0]['id']

        return self.user_id

    def get_user_friends(self):
        data = dict(user_id=self.user_id, fields='bdate')
        friends_data = self.get(method_name='friends.get', data=data)
        if friends_data['is_error']:
            return self.user_friends

        if 'response' in friends_data.keys() and friends_data['response']['count'] > 0:
            self.user_friends = friends_data['response']['items']
        return self.user_friends


def calc_age(uid):
    now = datetime.datetime.now()
    user = VKUser(uid)
    user.get_user()
    user.get_user_friends()
    ages = []
    friend_ages = []
    for item in  user.user_friends:
        if 'bdate' in item.keys() and re.match(r'.*\d{4}$', item['bdate']):
            ages.append(now.year - int(item['bdate'][-4:]))
    for i in set(ages):
        friend_ages.append((i, ages.count(i)))
    friend_ages.sort(key=lambda x: (-x[1], x[0]))
    return friend_ages


if __name__ == '__main__':
    res = calc_age('szueff')

    print(res)