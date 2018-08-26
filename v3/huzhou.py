import threading

import wanda_utils

TOKEN = '00707771d8232a2de49bb1a4189d57d7b5ea5b23'
PLAZAID = '1102223'
PROVINCE = '330000'
PLACE = '湖州'
LOCK = threading.Lock()

if __name__ == '__main__':
    wanda_utils.init(PLACE, TOKEN, PROVINCE, PLAZAID)
    wanda_utils.ui()
