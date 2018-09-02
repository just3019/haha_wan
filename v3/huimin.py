import wanda_utils

TOKEN = '007064165942ad7749271ead0a851d4ebefc0fb3'
PLAZAID = '1104483'
PROVINCE = ''
PLACE = '回民区'
XM_LOCAL = ""

if __name__ == '__main__':
    wanda_utils.init(PLACE, TOKEN, PROVINCE, PLAZAID, XM_LOCAL)
    wanda_utils.ui()
