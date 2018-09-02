import wanda_utils

TOKEN = '00756470bb663843d577317dc8882564f2185d58'
PLAZAID = '1103406'
PROVINCE = ''
PLACE = '北海'


if __name__ == '__main__':
    wanda_utils.init(PLACE, TOKEN, PROVINCE, PLAZAID)
    wanda_utils.ui()
