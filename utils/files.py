import datetime
import os
import random

from django.utils import timezone
from django.utils.deconstruct import deconstructible


@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        timestamp = int(datetime.datetime.now().timestamp())
        random_code = int(''.join([random.choice('123456789') for x in range(5)]))
        filename = '{}_{}.{}'.format(timestamp, random_code, ext)
        return os.path.join(self.path, filename)


