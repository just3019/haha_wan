import wanda_utils

TOKEN = '00779411d6db9499b1193cc842046c128bc6d298'
PLAZAID = '1103405'
PROVINCE = ''
PLACE = '南宁江南'
XM_LOCAL = ""

if __name__ == '__main__':
    wanda_utils.init(PLACE, TOKEN, PROVINCE, PLAZAID, XM_LOCAL)
    wanda_utils.ui()
