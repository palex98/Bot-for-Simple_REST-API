import json
import requests
import random
import string

with open('credentials.json', 'r', encoding='utf-8') as cred_file, \
        open('config.json', 'r', encoding='utf-8') as config_file:
    credentials = json.load(cred_file)
    config = json.load(config_file)

def random_string(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def auth(username=credentials['username'], password=credentials['password']):
    response = requests.post(f'{credentials["url"]}/auth', json={"username": username, "password": password})

    if response.status_code == 200:

        access_token = f'JWT {response.json()["access_token"]}'
        return access_token
    else:
        print('Error on getting JWT token')
        print(response.status_code)
        return

def users_signup(number_of_users):
    users = [{"username": f'user_{random_string(4)}', "password": random_string(8)} for _ in range(number_of_users)]
    for user in users:
        access_token = auth()
        response = requests.post(f'{credentials["url"]}/register', headers={"Authorization": access_token}, json=user)
        if response.status_code != 201:
            print('Error on creating users')
            print(response.text)
            return
    print('success on creating users')
    return users


def users_creating_random_posts(max_posts_per_user):
    access_token = auth()
    users = requests.get(f'{credentials["url"]}/users', headers={"Authorization": access_token})
    for user in users.json():
        for i in range(random.randint(1, max_posts_per_user)):
            access_token = auth(username=user["username"], password=user["password"])
            response = requests.post(f'{credentials["url"]}/post', headers={"Authorization": access_token},
                                     json={"text": random_string(20)})
            if response.status_code != 201:
                print('Error on creating posts')
                print(response.text)
                return
    print('success on creating posts')
    return 1


def like_random_posts(max_likes_per_user):
    access_token = auth()
    users = requests.get(f'{credentials["url"]}/users', headers={"Authorization": access_token})
    access_token = auth()
    posts = requests.get(f'{credentials["url"]}/posts', headers={"Authorization": access_token})

    for user in users.json():
        for i in range(random.randint(1, max_likes_per_user)):
            access_token = auth(username=user["username"], password=user["password"])
            response = requests.put(
                f'{credentials["url"]}/like/{random.choice([post["id"] for post in posts.json()])}',
                headers={"Authorization": access_token})
            if response.status_code not in (200, 201):
                print('Error on liking posts')
                print(response.text)
    print('succes on liking posts')
    return


def run_bot():
    users = users_signup(config['number_of_users'])
    if users:
        users_creating_random_posts(config['max_posts_per_user'])
        like_random_posts(config['max_likes_per_user'])
    return


run_bot()
