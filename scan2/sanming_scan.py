import threading

import wanpuxiaoer_utils

lock = threading.Lock()

place = "三明"

storeId = "100004201"
userid = "270126902395543552"
token = "MjcwNjQ4MTM4MjE3Mjk5OTY4"
client_code = "1fa17018de49498fb4406b2a480ae1c1"
place_id = "1102566"

if __name__ == '__main__':
    wanpuxiaoer_utils.check(client_code, place_id)
    wanpuxiaoer_utils.init(place, storeId, userid, token)
    wanpuxiaoer_utils.ui()