import os
import zipfile
import tarfile



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

            #全部解压
            # unzip.extractall(newfilepath)
            # print(unzip.namelist())
            # unzip.close()


            #一个一个解压
            for file in unzip.namelist():
                unzip.extract(file, newfilepath)
                print(file)
            unzip.close()


        elif ext == ".gz":
            untar = tarfile.open(filepath)

            # 全部解压
            # untar.extractall(newfilepath)
            # print(untar.getnames())
            # untar.close()


            # 一个一个解压
            for file in untar.getnames():
                untar.extract(file,newfilepath)
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
