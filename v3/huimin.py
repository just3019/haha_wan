import threading

import wanda_utils

TOKEN = '007064165942ad7749271ead0a851d4ebefc0fb3'
PLAZAID = '1104483'
PROVINCE = ''
PLACE = '回民区'
LOCK = threading.Lock()

if __name__ == '__main__':
    wanda_utils.init(PLACE, TOKEN, PROVINCE, PLAZAID)
    wanda_utils.ui()
