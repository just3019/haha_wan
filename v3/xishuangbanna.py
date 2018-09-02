import wanda_utils

TOKEN = '00747188e73e086af1e854f98992bfd2eb1fa4e6'
PLAZAID = '1000964'
PROVINCE = '530000'
PLACE = '西双版纳'
XM_LOCAL = ""

if __name__ == '__main__':
    wanda_utils.init(PLACE, TOKEN, PROVINCE, PLAZAID, XM_LOCAL)
    wanda_utils.ui()
