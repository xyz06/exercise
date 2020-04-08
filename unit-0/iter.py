import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--List', help='input a array', nargs='+')
parser.add_argument('--step', help='input a number', type=int)

args = parser.parse_args()


def iter_slice(iList, step):
    ltg = len(iList)
    no = 0
    while no < ltg:
        yield iList[no:(no // 2 + 1) * step]
        no += step


if __name__ == "__main__":

    for x in iter_slice(args.List, args.step):
        print(x)
