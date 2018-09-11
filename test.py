import re

if __name__ == '__main__':
    pat = "^1[7]\d{9}$"
    IC = re.search(pat, "13011111111")
    if IC:
        print(IC.group())
