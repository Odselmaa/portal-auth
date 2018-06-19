from model import *


def get_access_token(token):
    at = AccessToken.objects(token=token).first()
    return at


def add_access_token(payload):
    at = AccessToken.objects(user_id=payload['user_id']).first()
    if at:
        print(at.to_json())

        at.provider=payload['provider']
        at.token=payload['token']
        at.created_when=datetime.datetime.fromtimestamp(payload['created_when'])
        at.expired_when=datetime.datetime.fromtimestamp(payload['expired_when'])
        at.update()
    else:
        at = AccessToken(provider=payload['provider'],
                         token=payload['token'],
                         created_when=datetime.datetime.fromtimestamp(payload['created_when']),
                         expired_when=datetime.datetime.fromtimestamp(payload['expired_when']),
                         user_id=payload['user_id'])

        at.save()
    return at


def get_access_tokens():
    return AccessToken.objects