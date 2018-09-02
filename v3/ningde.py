import wanda_utils

TOKEN = '007460976176bc2fbf1946043accf467d2fc4516'
PLAZAID = '1000389'
PROVINCE = '350000'
PLACE = '宁德'


if __name__ == '__main__':
    wanda_utils.init(PLACE, TOKEN, PROVINCE, PLAZAID)
    wanda_utils.ui()
