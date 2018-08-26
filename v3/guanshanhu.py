import threading

import wanda_utils

TOKEN = '00747450004457336e169d24663545ec91402703'
PLAZAID = '1105295'
PROVINCE = '520000'
PLACE = '观山湖'
LOCK = threading.Lock()

if __name__ == '__main__':
    wanda_utils.init(PLACE, TOKEN, PROVINCE, PLAZAID)
    wanda_utils.ui()
