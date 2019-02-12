'''
@author: Evan
@email: lenguyenhoangvan18@gmail.com
@version: 1.0
@since: Feb 2, 2019
'''
# convert json to a python object
import json
from collections import namedtuple


def _json_object_hook(d):
    return namedtuple('X', d.keys())(*d.values())


def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)
