import json
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
    str = '{"status":200,"data":{"uid":"15000000275022050","member":{"pwid":300111000124102933,"nickName":"ffan2154","gender":0,"realName":"","headPortrait":"","puid":"A283D45AD75941FAA1B3AC7BB8A26D18","mobile":"13675822154"},"loginToken":"5396b9d2b9f044f8fcf2f0b7ccc43ad9","cookieStr":"psid=70216452f2973a5639f93536bf7a54ea; puid=A283D45AD75941FAA1B3AC7BB8A26D18; up=bup; sid=5396b9d2b9f044f8fcf2f0b7ccc43ad9; uid=15000000275022050; uniqkey2=RZhczLgfkoQJoTrJRUGWSZjyXYXi8FVdidII/7GuC1b31YxYxBjAFTFgrJfBUyzzmK7d4I8KAlNbEgWS8HQXx2ntWgdTxpyBCBwMdgJmKiT0WGl9f9822nTW3A0DCjRvRJ5xyjtmGqfPGdxI6wHsYTj3BtzlX2GP0Q7j9bI9yYmBHmH/dP9gVN7Y0M6WjtEaj9Lw; puid=A283D45AD75941FAA1B3AC7BB8A26D18; uid=15000000275022050; ploginToken=70216452f2973a5639f93536bf7a54ea; ","canConsolidate":0,"subStatus":1,"xmt_action":"login","ploginToken":"70216452f2973a5639f93536bf7a54ea","puid":"A283D45AD75941FAA1B3AC7BB8A26D18"},"message":"OK"}'
    jsonStr = json.loads(str)
    if "uid" in jsonStr["data"]:
        print("存在")
    else:
        print("不存在")
    # for i in range(1, 100):
    #     try:
    #         phone_sms()
    #     except RuntimeError as e:
    #         print(e)
            # pat = "^1[7]\d{9}$"
            # IC = re.search(pat, "13011111111")
            # if IC:
            #     print(IC.group())
