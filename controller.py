from model import *


def get_access_token(token):
    at = AccessToken.objects(token=token).first()
    return at

def add_access_token(payload):
    at = AccessToken(provider=payload['provider'],
                     token=payload['token'],
                     created_when=datetime.datetime.fromtimestamp(payload['created_when']),
                     expired_when=datetime.datetime.fromtimestamp(payload['expired_when']))
    at.save()
    return at