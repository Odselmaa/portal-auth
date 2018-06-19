from model import *


def get_access_token(token):
    at = AccessToken.objects(token=token).first()
    return at

