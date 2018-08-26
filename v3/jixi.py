import threading

import wanda_utils

TOKEN = '007056140310e2f0d4c284953feeb964b150d4cc'
PLAZAID = '1100573'
PROVINCE = '230000'
PLACE = '鸡西'
LOCK = threading.Lock()

if __name__ == '__main__':
    wanda_utils.init(PLACE, TOKEN, PROVINCE, PLAZAID)
    wanda_utils.ui()
