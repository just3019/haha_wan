import wanda_utils

TOKEN = ''
PLAZAID = '1103268'
PROVINCE = ''
PLACE = '益阳'


if __name__ == '__main__':
    wanda_utils.init(PLACE, TOKEN, PROVINCE, PLAZAID)
    wanda_utils.ui()
