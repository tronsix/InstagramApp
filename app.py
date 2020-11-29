import os
from dotenv import load_dotenv
import oauth2
import urllib.parse as urlparse
import json

from database import db
from user import User

dotenv_path = os.path.join('.env')
load_dotenv(dotenv_path)

KEY = os.environ.get('KEY')
SECRET = os.environ.get('SECRET')
ETSY_API = os.environ.get('ETSY_API')
REQUEST_URL = os.environ.get('REQUEST_URL')
SCOPE = os.environ.get('SCOPE')
ACCESS_URL = os.environ.get('ACCESS_URL')

# Create a consumer using our app key and secret
consumer = oauth2.Consumer(KEY, SECRET)
# Initialize DB
db.init(database='etsy', user='postgres', password='destiny123', host='localhost')

# Prompt user for email
email = input('Email: ')

try:
    user = User.load_from_db_by_email(email)
    # Set auth_token object using access token and secret. Create new auth client.
    auth_token = oauth2.Token(user.oauth_token, user.oauth_token_secret)
    auth_client = oauth2.Client(consumer, auth_token)
    res, content = auth_client.request(ETSY_API + 'users/__SELF__/shops')
    if res.status != 200:
        print('{} Error'.format(res.status))
    data = json.loads(content.decode('utf-8'))
    shops = data['results'][0]
    print(shops)

except: 
    client = oauth2.Client(consumer)

    # Use the client to perform a request for reequest token
    res, content = client.request(REQUEST_URL + SCOPE, 'GET')
    if res.status != 200:
        print('Error {}'.format(res.status))

    # Upon return parse request and print out login url
    req_token = dict(urlparse.parse_qsl(content.decode('utf-8')))
    print(req_token['login_url'])

    # Collect verifier pin
    oauth_verifier = input('What is the pin? ')

    # Create a token object using token, secret, and verifier
    token = oauth2.Token(req_token['oauth_token'], req_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)

    # Create a client using our verified token
    client = oauth2.Client(consumer, token)

    # Request access token using new client and access token url
    res, content = client.request(ACCESS_URL, 'GET')
    if res.status != 200:
        print('Error {}'.format(res.status))

    # Parse access token request
    access_token = dict(urlparse.parse_qsl(content.decode('utf-8')))

    # Set auth_token object using access token and secret. Create new auth client.
    auth_token = oauth2.Token(access_token['oauth_token'], access_token['oauth_token_secret'])
    auth_client = oauth2.Client(consumer, auth_token)

    # Make authorized request to get user profile
    res, content = auth_client.request('https://openapi.etsy.com/v2/users/__SELF__/profile', 'GET')
    if res.status != 200:
        print('Error {}'.format(res.status))

    data = json.loads(content.decode('utf-8'))
    user_profile = data['results'][0]

    new_user = User(user_profile['user_id'], email, user_profile['first_name'], 
    user_profile['last_name'], access_token['oauth_token'], access_token['oauth_token_secret'], None)

    new_user.save_to_db()