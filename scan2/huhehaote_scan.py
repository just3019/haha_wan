import threading

import wanpuxiaoer_utils

lock = threading.Lock()

place = "呼和浩特"

storeId = "100004997"
userid = "266207569143951360"
token = "MjcwNjQ2MzIxODczOTUyNzY4"
client_code = "1fa17018de49498fb4406b2a480ae1c1"
place_id = "1000303"

if __name__ == '__main__':
    wanpuxiaoer_utils.check(client_code, place_id)
    wanpuxiaoer_utils.init(place, storeId, userid, token)
    wanpuxiaoer_utils.ui()
