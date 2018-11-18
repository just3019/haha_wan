import threading

import wanpuxiaoer_utils

lock = threading.Lock()

place = "滨州"

storeId = "100000251"
userid = "269129928065794048"
token = "MjY5Nzg1OTczMDY3NjAzOTY4"
client_code = "12023a7d74f447fab227213f52c970f8"
place_id = "1102461"

if __name__ == '__main__':
    wanpuxiaoer_utils.check(client_code, place_id)
    wanpuxiaoer_utils.init(place, storeId, userid, token)
    wanpuxiaoer_utils.ui()
