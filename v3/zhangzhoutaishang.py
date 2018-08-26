import threading

import wanda_utils

TOKEN = '00753103e21ff2b50ebdac2ddf45040cd97db172'
PLAZAID = '1100810'
PROVINCE = '350000'
PLACE = '漳州台商'
LOCK = threading.Lock()

if __name__ == '__main__':
    wanda_utils.init(PLACE, TOKEN, PROVINCE, PLAZAID)
    wanda_utils.ui()
