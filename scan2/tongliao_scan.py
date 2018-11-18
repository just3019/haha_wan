import threading

import wanpuxiaoer_utils

lock = threading.Lock()

place = "通辽"

storeId = "100006884"
userid = "269038101515313152"
token = "MjcwNjQ4NzMzMDExMzgyMjcy"
client_code = "af603439c5f54e63984e7a71e947d4c4"
place_id = "1100789"

if __name__ == '__main__':
    wanpuxiaoer_utils.check(client_code, place_id)
    wanpuxiaoer_utils.init(place, storeId, userid, token)
    wanpuxiaoer_utils.ui()