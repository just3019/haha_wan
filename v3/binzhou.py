import wanda_utils

TOKEN = '00798999d856a74e9cd0b4257da5590a0a382712'
PLAZAID = '1102461'
PROVINCE = ''
PLACE = '滨州'


if __name__ == '__main__':
    wanda_utils.init(PLACE, TOKEN, PROVINCE, PLAZAID)
    wanda_utils.ui()
