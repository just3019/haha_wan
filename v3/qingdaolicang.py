import wanda_utils

TOKEN = ''
PLAZAID = '1000396'
PROVINCE = ''
PLACE = '青岛李沧'
XM_LOCAL = ""
HM_PROVINCE = ""

if __name__ == '__main__':
    wanda_utils.init(PLACE, TOKEN, PROVINCE, PLAZAID, HM_PROVINCE, XM_LOCAL)
    wanda_utils.ui()
