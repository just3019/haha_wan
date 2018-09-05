import wanda_utils

TOKEN = ''
PLAZAID = '1102588'
PROVINCE = ''
PLACE = '北京丰台'
XM_LOCAL = ""
HM_PROVINCE = ""

if __name__ == '__main__':
    wanda_utils.init(PLACE, TOKEN, PROVINCE, PLAZAID, HM_PROVINCE, XM_LOCAL)
    wanda_utils.ui()
