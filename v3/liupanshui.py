import wanda_utils

TOKEN = '007763861350c65a82c03579a25bb1bd0dee1ca4'
PLAZAID = '1105208'
PROVINCE = ''
PLACE = '六盘水'


if __name__ == '__main__':
    wanda_utils.init(PLACE, TOKEN, PROVINCE, PLAZAID)
    wanda_utils.ui()
