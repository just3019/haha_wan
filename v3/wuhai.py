import wanda_utils

TOKEN = '0078671539735bcd879c4febe26fa8d2a888002b'
PLAZAID = '1100754'
PROVINCE = ''
PLACE = '乌海'
XM_LOCAL = ""

if __name__ == '__main__':
    wanda_utils.init(PLACE, TOKEN, PROVINCE, PLAZAID, XM_LOCAL)
    wanda_utils.ui()
