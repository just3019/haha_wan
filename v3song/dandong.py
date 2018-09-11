import wanda_utils

TOKEN = ''
PLAZAID = '1000625'
PROVINCE = '210000'
PLACE = '丹东'
XM_LOCAL = "辽宁"
HM_PROVINCE = "辽宁"

if __name__ == '__main__':
    wanda_utils.init(PLACE, TOKEN, PROVINCE, PLAZAID, HM_PROVINCE, XM_LOCAL)
    wanda_utils.ui()
