import threading

import wanpuxiaoer_utils

lock = threading.Lock()

place = "乌海"

storeId = "100007997"
userid = "269030028967788544"
token = "MjcxMzMwMDE4NjA4Mzg2MDQ4"
client_code = "ce29d3f9a67847c09827f6673934eff7"
place_id = "1100754"

if __name__ == '__main__':
    wanpuxiaoer_utils.check(client_code, place_id)
    wanpuxiaoer_utils.init(place, storeId, userid, token)
    wanpuxiaoer_utils.ui()