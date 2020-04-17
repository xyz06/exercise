import os
import random
import time
import json
import re
import urllib.request

import pymongo
import yaml
from bs4 import BeautifulSoup
import argparse
import platform

allInfo = []  # use cmd() after, get data
ports = ["443", "80"]  # not check port
ips = ["0.0.0.0", "[::]", "*", "127.0.0.1", "[::1]"]  # not spider geoip
pids = []
datas = []


def info_filter(info):
    start = re.search("(TCP | UDP)", info, re.I)
    info = info[start.end():]
    get_info(info)


def get_info(info):
    global allInfo
    oneInfo = []  # filter after one info
    start = re.search("(TCP | UDP)", info, re.I)
    if start == None:
        msg = info
    else:
        msg = info[:start.start()]
    oneList = msg.strip(" ").strip("\n").split(" ")
    for i in oneList:
        if not i and i != "0":
            oneInfo.append(i)
    if not start:
        return
    else:
        restInfo = info[start.end():]
    allInfo.append(oneInfo)
    get_info(restInfo)


def cmd(systemType):
    if systemType == "Linux":
        info = os.popen("netstat -tunlp").read()
    elif systemType == "Windows":
        info = os.popen("netstat -ano").read()
    # elif systemType == "Mac":
    #     info = os.popen().read()
    info_filter(info)


def spider_geoip(ip):
    try:
        url = "https://www.ip.cn/?ip=" + ip
        ua_list = [
        "Mozilla / 5.0(Windows NT 6.1; Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 78.0.3904.108 Safari / 537.36"
        " Mozilla / 5.0(Windows NT 6.1;WOW64) AppleWebKit / 535.1(KHTML, like Gecko) Chrome / 14.0835.163 Safari / 535.1"
        "Mozilla / 5.0(Macintosh; Intel Mac OSX10_7_0) AppleWebKit / 535.11(KHTML, like Gecko) Chrome / 17.0.963.56 Safari / 535.11"
        "Opera / 9.80(Windows NT 6.1; U ; en) Presto / 2.8.131 Version / 11.11"
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"
        ]
        req = urllib.request.Request(url, headers={'User-Agent': random.choice(ua_list)})
        data = urllib.request.urlopen(req, timeout=20).read().decode()

        soup = BeautifulSoup(data, "html.parser")
        p = soup.select("div[class='well'] p")[-1]
        geoip = p.select("code")[0].text
        return geoip

    except Exception as err:
        print("[Error]:", err)


def get_data(systemType):
    global datas
    global allInfo
    global ips

    for i in allInfo:
        ipPort = i[1]
        p = ipPort.rindex(":")
        port = ipPort[p + 1:]

        ip = ipPort[:p]

        if systemType == "Linux":
            pp = i[-1].split("/")
            pid = pp[0]
            processName = pp[1]
        elif systemType == "Windows":
            pid = i[-1]

        data = {}
        if port not in ports and pid not in pids and ip not in ips:
            pids.append(pid)
            geoip = spider_geoip(ip)
            data['pid'] = pid
            if systemType == "Linux":
                data['process_name'] = processName
            elif systemType == "Windows":
                data['process_name'] = find_processName(pid)
            data['ip'] = ip
            data['geoip'] = geoip
            data['timestamp'] = time.time()
            datas.append(data)
    return datas


def find_processName(pid):
    cmd = os.popen("tasklist |findstr %s" % pid)
    da = cmd.read()
    if da == "":
        return False
    else:
        li = da.split(" ")
        return li[0]


def write_file(out, data):
    if not os.path.exists(out):
        f = open(out, "w")
    else:
        f = open(out, "a+")

    for d in data:
        f.write(json.dumps(d) + "\n")
    f.close()
    print("Write file successful")
    return


def write_mongo(data, yamlpath):
    with open(yamlpath, "r") as f:
        cfg = yaml.load(f.read(), yaml.FullLoader)
    if cfg['user']:
        myclient = pymongo.MongoClient("mongodb://%s:%s@%s:%s/" % (
            cfg['user'], cfg['password'], cfg['host'], cfg['port']))
    else:
        myclient = pymongo.MongoClient("mongodb://%s:%s/" % (cfg['host'], cfg['port']))

    mydb = myclient["xyz"]
    mycol = mydb['checkport']
    mycol.insert_many(data)
    print("Write mongo successful")
    return


def process(out, config, systemType):
    global datas
    try:
        cmd(systemType)
        get_data(systemType)
        if datas:
            write_file(out, datas)
            write_mongo(datas, config)
        else:
            print("Port not occupied")
    except Exception as err:
        print(err)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=str, help="input a filepath", required=True)
    parser.add_argument("--config", type=str, help="input a mongo config", required=True)
    args = parser.parse_args()
    systemType = platform.system()
    if os.path.exists(args.config):
        process(args.out, args.config, systemType)
    else:
        print("[Error]:config no exist")
