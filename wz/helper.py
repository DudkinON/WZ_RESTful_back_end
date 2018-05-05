from __future__ import unicode_literals

import hashlib
import os
from random import random
from json import dumps
from .settings import STORY_IMG_ROOT, USER_IMAGES_ROOT
from random import choice
from string import ascii_uppercase as uppercase, digits


def get_path(instance, filename, folder):
    """
    Generate a unique path for image
    :param instance: object
    :param filename: string
    :param folder: string
    :return string: string
    """
    ext = filename.split('.')[-1]
    hash_ = hashlib.md5()
    hash_.update(repr(random()).encode('utf-8'))
    hash_name = hash_.hexdigest()
    path_to_img = os.path.join(folder, hash_name[:2], hash_name[2:4],
                               hash_name[4:6])
    filename = '{0}.{1}'.format(hash_name[6:], ext)
    return '{0}/{1}'.format(path_to_img, filename)


def get_image_path(instance, filename):
    """Return path for article image
    :param instance: object
    :param filename: string
    :return: string
    """
    return get_path(instance, filename, STORY_IMG_ROOT)
