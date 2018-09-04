import wanda_utils

TOKEN = ''
PLAZAID = '1100810'
PROVINCE = '350000'
PLACE = '漳州台商'
XM_LOCAL = ""
HM_PROVINCE = ""

if __name__ == '__main__':
    wanda_utils.init(PLACE, TOKEN, PROVINCE, PLAZAID, HM_PROVINCE, XM_LOCAL)
    wanda_utils.ui()
