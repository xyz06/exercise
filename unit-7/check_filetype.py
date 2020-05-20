import struct
import filetype
import argparse

TYPES = {
    "FFD8FF": "JPEG",
    "89504E47": "PNG",
    "49443303": "MP3",
    "00000020": "MP4"
}

def bytes2hex(bytes):
    num = len(bytes)
    hexstr = u""
    for i in range(num):
        t = u"%x" % bytes[i]
        if len(t) % 2:
            hexstr += u"0"
        hexstr += t
    return hexstr.upper()


def file_type(filepath):
    try:
        binfile = open(filepath, "rb")
        ftype = "unknow"
        for hcode in TYPES.keys():
            numOfBytes = len(hcode) // 2
            binfile.seek(0)
            hbytes = struct.unpack_from("B" * numOfBytes, binfile.read(numOfBytes))
            f_hcode = bytes2hex(hbytes)
            if f_hcode == hcode:
                ftype = TYPES[hcode]
                break
        binfile.close()
        return ftype
    except Exception as err:
        print(err)


def file_type_1(filepath):
    try:
        f = filetype.guess(filepath)
        ftype = f.mime.split("/")[1]
        return ftype
    except Exception as err:
        print(err)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--filepath", type=str, required=True)
    arg = parser.parse_args()
    print(file_type(arg.filepath))
    # print(file_type_1(arg.filepath))