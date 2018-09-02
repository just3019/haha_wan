import wanda_utils

TOKEN = '0070559089f4587e40104e6768bd06ebebb4202b'
PLAZAID = '1100650'
PROVINCE = ''
PLACE = '台州'
XM_LOCAL = ""

if __name__ == '__main__':
    wanda_utils.init(PLACE, TOKEN, PROVINCE, PLAZAID, XM_LOCAL)
    wanda_utils.ui()
