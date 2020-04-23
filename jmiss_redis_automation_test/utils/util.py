# coding:utf-8
import socket
import array
import struct
import fcntl
import sys, os
import platform
import hashlib
import base64
import random


def format_ip(addr):
    return str(ord(addr[0])) + '.' + \
           str(ord(addr[1])) + '.' + \
           str(ord(addr[2])) + '.' + \
           str(ord(addr[3]))


def all_interfaces():
    max_possible = 128  # arbitrary. raise if needed.
    bytes = max_possible * 32
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    names = array.array('B', '\0' * bytes)
    outbytes = struct.unpack('iL', fcntl.ioctl(
        s.fileno(),
        0x8912,  # SIOCGIFCONF
        struct.pack('iL', bytes, names.buffer_info()[0])
    ))[0]
    namestr = names.tostring()
    ni_dict = {}
    for i in range(0, outbytes, 40):
        name = namestr[i:i + 16].split('\0', 1)[0]
        ip = namestr[i + 20:i + 24]
        ni_dict[name] = format_ip(ip)
    return ni_dict


# 获取本地IP
def get_local_ip():
    if platform.system() == 'Darwin' or platform.system() == 'Windows':
        return "192.168.162.16"
    nw_dict = all_interfaces()
    local_ip = None
    ip_192 = None
    ip_172 = None
    for name, ip in nw_dict.items():
        local_ip = ip
        if ip.startswith("172.") and not name.startswith("docker"):
            ip_172 = ip
            break
    for name, ip in nw_dict.items():
        if ip.startswith("192.") and not name.startswith("docker"):
            ip_192 = ip
            break
    if ip_172 is not None:
        local_ip = ip_172
    elif ip_192 is not None:
        local_ip = ip_192
    return local_ip


# 获取当前文件的绝对路径
def cur_file_dir():
    path = sys.path[0]
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)


# jmiss-web密码加密
def get_md5_pwd(password):
    m = hashlib.md5()
    m.update(password)
    pwd_md5 = m.digest()
    pwd_base64 = base64.b64encode(pwd_md5)
    return pwd_base64

def get_shard_id(total, num):
    select_list = range(0, total)
    return random.sample(select_list, num)
