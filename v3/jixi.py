import wanda_utils

TOKEN = '00751415a46cbd33db93d78e7d4ea4c47d87dfff'
PLAZAID = '1100573'
PROVINCE = ''
PLACE = '鸡西'


if __name__ == '__main__':
    wanda_utils.init(PLACE, TOKEN, PROVINCE, PLAZAID)
    wanda_utils.ui()
