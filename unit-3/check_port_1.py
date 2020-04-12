import os
import random
import time
import json
import re
import urllib.request
from bs4 import BeautifulSoup
import argparse

allinfo = []                            # use cmd() after, get data
ports = ["443", "80"]                    # not check port
ips = ["0.0.0.0", "[::]", "*", "127.0.0.1", "[::1]"]     # not spider geoip
pids = []
datas = []


def info_filter(info):
    start = re.search("(TCP | UDP)", info, re.I)
    info = info[start.end():]
    get_info(info)


def get_info(info):
    global allinfo
    oneinfo = []  # filter after one info
    start = re.search("(TCP | UDP)", info, re.I)
    if start == None:
        msg = info
    else:
        msg = info[:start.start()]
    onelist = msg.strip(" ").strip("\n").split(" ")

    for i in range(0, len(onelist)):
        if onelist[i] != '':
            if onelist[i] != '0':
                oneinfo.append(onelist[i])
    allinfo.append(oneinfo)
    try:
        endinfo = info[start.end():]
    except:
        return

    get_info(endinfo)

def cmd():
    if os.name == "posix":
        info = os.popen("netstat -tunlp").read()
    else:
        info = os.popen("netstat -ano").read()
    info_filter(info)

def spider_geoip(ip):
    url = "https://www.ip.cn/?ip=" + ip
    ua_list = [
        "Mozilla / 5.0(Windows NT 6.1; Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 78.0.3904.108 Safari / 537.36"
        " Mozilla / 5.0(Windows NT 6.1;WOW64) AppleWebKit / 535.1(KHTML, like Gecko) Chrome / 14.0835.163 Safari / 535.1"
        "Mozilla / 5.0(Macintosh; Intel Mac OSX10_7_0) AppleWebKit / 535.11(KHTML, like Gecko) Chrome / 17.0.963.56 Safari / 535.11"
        "Opera / 9.80(Windows NT 6.1; U ; en) Presto / 2.8.131 Version / 11.11"
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"
    ]
    req = urllib.request.Request(url, headers={'User-Agent': random.choice(ua_list)})
    data = urllib.request.urlopen(req,timeout=20).read().decode()
    try:
        soup = BeautifulSoup(data, "html.parser")
        p = soup.select("div[class='well'] p")[-1]
        geoip = p.select("code")[0].text
        return geoip

    except Exception as err:
        print("[Error]:",err)


def get_data():
    global datas
    global allinfo
    global ips

    for i in allinfo:
        tcp = i[1]
        p = tcp.rindex(":")
        port = tcp[p + 1:]

        ip = tcp[:p]

        if os.name == "posix":
            pp = i[-1].split("/")
            pid = pp[0]
            processName = pp[1]
        else:
            pid = i[-1]

        data = {}
        if port not in ports and pid not in pids and ip not in ips:
            pids.append(pid)
            geoip = spider_geoip(ip)
            data['pid'] = pid
            if os.name == "posix":
                data['process_name'] = processName
            else:
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


def write_data(out, data):
    if not os.path.exists(out):
        f = open(out, "w")
    else:
        f = open(out, "a")

    for d in data:
        f.write(json.dumps(d) + "\n")
    f.close()
    print("successful")
    return


def process(out):
    try:
        cmd()
        get_data()
        write_data(out, datas)
    except Exception as err:
        print(err)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=str, help="input a filepath")
    arg = parser.parse_args()
    if arg.out:
        process(arg.out)
    else:
        print("[Error]:Missing parameter")








