import re
import argparse


def print_with_width(text, width=80):
    n = width
    print(text[0:n])
    while n < len(text):

        if re.search(r"[a-zA-Z]", text[n]):
            if text[n - 1] == " ":
                print(text[n:n + width])
                n = n + width
            else:
                print("-", end="")
                print(text[n:n + width - 1])
                n = n + width - 1
        else:
            if text[n] == " ":
                print(text[n + 1:n + 1 + width])
                n = n + 1 + width
            else:
                print(text[n:n + width])
                n = n + width


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", type=str, required=True, help="input some English words")
    parser.add_argument("--width", type=int, default=80, help="it is per line width")
    args = parser.parse_args()
    print_with_width(args.text, args.width)
