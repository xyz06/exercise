import chardet
import os, shutil
import argparse

def get_code(file):
    f = open(file, "rb")
    data = f.read()
    f.close()
    chardet_1 = chardet.detect(data)
    return chardet_1['encoding']

def move_file(path, files):
    if not os.path.exists(path):
        os.makedirs(path)
    for f in files:
        shutil.move(f, os.path.join(path, f))

def split_file(file, line, name, dir):
    code = get_code(file)
    with open(file, "r", encoding=code) as f:
        lines = f.readlines()
        count = len(lines)
    if count % line == 0:
        file_total = count // line
    else:
        file_total = count // line + 1

    p = file.rindex(".")
    ext = file[p:]
    files = []

    for n in range(0, file_total):
        filename = ("%s.%d%s" % (name, n, ext))
        files.append(filename)
        wf = open(filename, "w", encoding=code)
        for row in range(n * line, n * line + line):
            if row < count:
                wf.write(lines[row])
            else:
                no = row
                break
        wf.close()
        if no == count:
            break
    move_file(dir,files)


if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument("--file", type=str, required=True)
    parse.add_argument("--line", type=int, required=True, help="The number of lines in the file")
    parse.add_argument("--name", type=str, required=True, help="New file name")
    parse.add_argument("--dir", type=str, required=True, help="New file store the path")
    args = parse.parse_args()
    split_file(args.file, args.line, args.name, args.dir)


