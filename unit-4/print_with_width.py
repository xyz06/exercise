import re
import argparse

def fristword_upper(text):
    words = text[0].upper()
    eof = [".", "!", "?", "......", "\""]
    for i in range(1, len(text)):
        if text[i-1] in eof:
            words += text[i].upper()
        elif text[i-2] in eof and i-2 > 0:
            words += text[i].upper()
        else:
            words += text[i]
    return words

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



