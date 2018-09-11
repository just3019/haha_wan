import wanda_utils

TOKEN = ''
PLAZAID = '1000769'
PROVINCE = '330000'
PLACE = '平阳'
XM_LOCAL = "浙江"
HM_PROVINCE = "浙江"

if __name__ == '__main__':
    wanda_utils.init(PLACE, TOKEN, PROVINCE, PLAZAID, HM_PROVINCE, XM_LOCAL)
    wanda_utils.ui()
