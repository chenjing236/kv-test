from string import *
from list import *
from set import *
from hash import *
from scan import *

cases = ['set_keys',
         'lpush_keys', 'rpush_keys',
         'sadd_keys', 'zadd_keys',
         'hset_keys',
         'scan_keys'
         ]

# case execute times
case_num = {}
for c in cases:
    case_num[c] = 0
