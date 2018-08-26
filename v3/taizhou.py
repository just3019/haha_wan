import threading

import wanda_utils

TOKEN = '0070559089f4587e40104e6768bd06ebebb4202b'
PLAZAID = '1100650'
PROVINCE = ''
PLACE = '台州'
LOCK = threading.Lock()

if __name__ == '__main__':
    wanda_utils.init(PLACE, TOKEN, PROVINCE, PLAZAID)
    wanda_utils.ui()
