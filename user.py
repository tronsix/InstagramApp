from database import ConnectionFromPool

class User:
    def __init__(self, user_id, email, first_name, last_name, oauth_token, oauth_token_secret, id):
        self.user_id = user_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        self.id = id

    def __repr__(self):
        return { 'id': self.id, 'user_id': self.user_id, 'email': self.email }

    def save_to_db(self):
        with ConnectionFromPool() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute('INSERT INTO users (user_id, email, first_name, last_name, oauth_token, oauth_token_secret) VALUES (%s, %s, %s, %s, %s, %s)',
                    (self.user_id, self.email, self.first_name, self.last_name, self.oauth_token, self.oauth_token_secret))
                    return print("User {} saved successfully".format(self.user_id))
                except:
                    print('Error')


    @classmethod
    def load_from_db_by_email(cls, email):
        with ConnectionFromPool() as connection:
            with connection.cursor() as cursor:
                cursor.execute('Select * from users where email = %s', (email,))
                userData = cursor.fetchone()
                return cls(user_id=userData[1], email=userData[2], first_name=userData[3], 
                           last_name=userData[4], oauth_token=userData[5], 
                           oauth_token_secret=userData[6], id=userData[0])
