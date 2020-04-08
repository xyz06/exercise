import os
import zipfile
import tarfile
import argparse

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('filepath', type=str, help='input one filepath')

arg = parser.parse_args()

def unpack(filepath):
    p = filepath.rindex('.')
    ext = filepath[p:]
    if ext == ".gz":
        newfilepath = filepath[:p - 4]
    else:
        newfilepath = filepath[:p]

    try:
        if ext == ".zip":
            unzip = zipfile.ZipFile(filepath)

            # all decompress
            # unzip.extractall(newfilepath)
            # print(unzip.namelist())
            # unzip.close()

            #  one by on Decompress
            for file in unzip.namelist():
                unzip.extract(file, newfilepath)
                print(file)
            unzip.close()


        elif ext == ".gz":
            untar = tarfile.open(filepath)

            # all decompress
            # untar.extractall(newfilepath)
            # print(untar.getnames())
            # untar.close()

            # one by one decompress
            for file in untar.getnames():
                untar.extract(file, newfilepath)
                print(file)
            untar.close()

    except Exception as err:
        print(err)


def zip(path):
    flist = []
    for file in os.listdir(path):
        if os.path.isdir(file):
            zip(os.path.join(path, file))
        else:
            flist.append(os.path.join(path, file))
    fzip = zipfile.ZipFile(path + ".zip", "w")
    for f in flist:
        fzip.write(f)
    fzip.close()


def tar(path):
    t = tarfile.open(path + ".tar.gz", "w:gz")
    for root, dir, files in os.walk(path):
        for file in files:
            pathfile = os.path.join(root, file)
            t.add(pathfile)
        print(root, dir, files)
    t.close()


if __name__ == "__main__":
    unpack(arg.filepath)