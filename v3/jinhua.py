import wanda_utils

TOKEN = '00499849cbf687835af75182698438eb3c2ccdf4'
PLAZAID = '1000685'
PROVINCE = '330000'
PLACE = '金华'
XM_LOCAL = ""

if __name__ == '__main__':
    wanda_utils.init(PLACE, TOKEN, PROVINCE, PLAZAID, XM_LOCAL)
    wanda_utils.ui()
