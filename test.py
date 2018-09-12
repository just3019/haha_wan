import random
import re

not_eq = 0


def phone_sms():
    # 当为1的时候从易码获取，当为其他的时候从讯码获取
    global not_eq
    num = random.randint(1, 3)
    if num == 1 and num != not_eq:
        print("本次易码获取号码")
        not_eq = 1
    elif num == 2 and num != not_eq:
        print("本次讯码获取号码")
        not_eq = 2
    elif num == 3 and num != not_eq:
        print("本次海码获取号码")
        not_eq = 3
    else:
        raise RuntimeError("重新选平台")


if __name__ == '__main__':
    for i in range(1, 100):
        try:
            phone_sms()
        except RuntimeError as e:
            print(e)
            # pat = "^1[7]\d{9}$"
            # IC = re.search(pat, "13011111111")
            # if IC:
            #     print(IC.group())
