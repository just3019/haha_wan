import threading

import wanda_utils

TOKEN = '00499849cbf687835af75182698438eb3c2ccdf4'
PLAZAID = '1102432'
PROVINCE = ''
PLACE = '成都青羊'
LOCK = threading.Lock()

if __name__ == '__main__':
    wanda_utils.init(PLACE, TOKEN, PROVINCE, PLAZAID)
    wanda_utils.ui()