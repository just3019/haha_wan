import wanda_utils

TOKEN = '00747256bbf22fef15006339d1d5d412681dd763'
PLAZAID = '1104655'
PROVINCE = '500000'
PLACE = '重庆北碚'
XM_LOCAL = ""

if __name__ == '__main__':
    wanda_utils.init(PLACE, TOKEN, PROVINCE, PLAZAID, XM_LOCAL)
    wanda_utils.ui()
