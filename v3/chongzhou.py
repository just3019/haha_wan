import wanda_utils

TOKEN = '007373010e787df886c6a246f5877fec161a9316'
PLAZAID = '1104507'
PROVINCE = '510000'
PLACE = '崇州'
XM_LOCAL = ""

if __name__ == '__main__':
    wanda_utils.init(PLACE, TOKEN, PROVINCE, PLAZAID, XM_LOCAL)
    wanda_utils.ui()
