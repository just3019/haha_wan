import wanda_utils

TOKEN = '0072891891c7981d81cb2918b3b22a879064d4af'
PLAZAID = '1102566'
PROVINCE = '350000'
PLACE = '三明'
XM_LOCAL = ""

if __name__ == '__main__':
    wanda_utils.init(PLACE, TOKEN, PROVINCE, PLAZAID, XM_LOCAL)
    wanda_utils.ui()
