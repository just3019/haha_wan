import wanda_utils

TOKEN = ''
PLAZAID = '1100650'
PROVINCE = ''
PLACE = '台州'
XM_LOCAL = ""
HM_PROVINCE = ""

if __name__ == '__main__':
    wanda_utils.init(PLACE, TOKEN, PROVINCE, PLAZAID, HM_PROVINCE, XM_LOCAL)
    wanda_utils.ui()
