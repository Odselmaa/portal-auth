from bson import json_util
from mongoengine import *
import datetime

class CustomQuerySet(QuerySet):
    def to_json(self):
        return "[%s]" % (",".join([doc.to_json() for doc in self]))


class AccessToken(Document):

    provider = StringField(required=True)
    token = StringField(required=True)
    created_when = DateTimeField(required=True, default=datetime.datetime.now())
    expired_when = DateTimeField(required=True)

    meta = {'queryset_class': CustomQuerySet}

    def to_json(self):
        data = self.to_mongo()
        print(self)
        data['expired_when'] = data['expired_when'].timestamp()
        data['created_when'] = data['created_when'].timestamp()
        return json_util.dumps(data)
