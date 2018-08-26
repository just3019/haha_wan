import threading

import wanda_utils

TOKEN = '0078671539735bcd879c4febe26fa8d2a888002b'
PLAZAID = '1100754'
PROVINCE = ''
PLACE = '乌海新人礼'
LOCK = threading.Lock()

if __name__ == '__main__':
    wanda_utils.init(PLACE, TOKEN, PROVINCE, PLAZAID)
    wanda_utils.xinren_ui()
