import threading

import wanda_utils

TOKEN = '00747256bbf22fef15006339d1d5d412681dd763'
PLAZAID = '1104655'
PROVINCE = '500000'
PLACE = '重庆北碚'
LOCK = threading.Lock()

if __name__ == '__main__':
    wanda_utils.init(PLACE, TOKEN, PROVINCE, PLAZAID)
    wanda_utils.ui()
