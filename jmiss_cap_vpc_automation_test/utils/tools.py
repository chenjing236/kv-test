#!/usr/bin/env python 
# coding=utf-8


def en_decode_encode(str):
    if isinstance(str, unicode):
        return str.encode('gb2312')
    else:
        return str.decode('utf-8').encode('gb2312')
