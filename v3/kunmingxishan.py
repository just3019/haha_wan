import wanda_utils

TOKEN = '007711720862de70a346fc1788db353c18c5d478'
PLAZAID = '1000744'
PROVINCE = ''
PLACE = '昆明西山'
XM_LOCAL = ""

if __name__ == '__main__':
    wanda_utils.init(PLACE, TOKEN, PROVINCE, PLAZAID, XM_LOCAL)
    wanda_utils.ui()
