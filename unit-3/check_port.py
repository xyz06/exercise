import os
import time
import json
import argparse

info = []               #use cmd() after, get data
ports = ['443', '80']   #not check port
pids = []
datas = []


def cmd():
    global info
    os.popen("netstat -ano > a.txt")
    f = open('a.txt', "r")
    for li in f:
        info.append(li.strip(" ").strip("\n"))
    f.close()


def get_data():
    global datas
    global info

    for i in range(4, len(info)):
        d = info[i].split(" ")
        port = d[4]
        p = port.rindex(":")
        port = port[p + 1:]

        pid = d[-1]
        data = {}
        if port not in ports and pid not in pids:
            pids.append(pid)
            data['pid'] = pid
            data['process_name'] = fpid(pid)
            data['timestamp'] = time.time()
            datas.append(data)
    return datas


def fpid(pid):
    cmd = os.popen("tasklist |findstr %s" % pid)
    da = cmd.read()
    if da == "":
        return False;
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


def deltempfile():
    time.sleep(2)
    os.remove("a.txt")


def process(out):
    global info
    try:
        cmd()
        get_data()
        write_data(out, datas)
        deltempfile()
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

