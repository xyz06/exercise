import re
import argparse


def firstword_uppper(text):
    eof = [".", "!", "?", '"']
    new_text = ''
    need_upper = True
    for c in text:
        if c in eof:
            need_upper = True
        elif c == ",":
            need_upper = False
        else:
            if need_upper and ('a' <= c <= 'z' or 'A' <= c <= 'Z'):
                c = c.upper()
                need_upper = False
        new_text += c

    return new_text


def print_with_width(text, width, paragraph):
    n = width
    if paragraph == True:
        words = fristword_upper(text)
    else:
        words = text

    print(words[0:n])
    while n < len(words):
        if re.search(r"[a-zA-Z]", words[n]):
            if words[n - 1] == " ":
                print(words[n:n + width])
                n = n + width
            else:
                print("-", end="")
                print(words[n:n + width - 1])
                n = n + width - 1
        else:
            if words[n] == " ":
                print(words[n + 1:n + 1 + width])
                n = n + 1 + width
            else:
                print(words[n:n + width])
                n = n + width



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", type=str, required=True, help="input some English words")
    parser.add_argument("--width", type=int, default=80, help="it is per line width")
    parser.add_argument("--paragraph", default="False", action="store_true")
    args = parser.parse_args()
    print_with_width(args.text, args.width, args.paragraph)



