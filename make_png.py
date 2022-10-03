from PIL import Image
import qrcode
from os.path import dirname, join

# Constants
POS_DIREC = "in.png"
FILE_TYPE = ".png"
QRC_DIREC = ".\\qr\\"

def paste_qr(post_path, qr_path, out_path):
    try:
        print("Loading: " + post_path)
        oriImg = Image.open(post_path)
        # addImg(oriImg)
        print("Loading: " + qr_path)
        qrcImg = Image.open(qr_path)
        qrcImg = qrcImg.resize((1000, 1000), Image.ANTIALIAS)
        oriImg.paste(qrcImg,(3000,5000))
        oriImg.save(out_path)

        # oriImg.show()
    except IOError:
        print("can't open the file,check the path again\n")
        newImg = Image.new('RGBA',(320,240),'blue')
        newImg.save(out_path)


def makea_qr(code, name):
    out_path = QRC_DIREC + name + FILE_TYPE
    out_path = join(dirname(__file__), out_path)
    qr = qrcode.QRCode(
        version = None, # Make it as tiny as possible
        error_correction = qrcode.constants.ERROR_CORRECT_L,
        box_size=100, # HD
        border = 5
    )
    try:
        print("Making QRcode for {} with value :{}".format(name,code))
        qr.add_data(code)
        qr.make(fit = True)
        newImg = qr.make_image()
        newImg.save(out_path)
        # newImg.show()


    except:
        print("can't create qr code,check priv\n")
        newImg = Image.new('RGBA',(320,240),'blue')
        newImg.save(out_path)

# for single use
if __name__ == '__main__':
    tmp_code = input("code: ")
    tmp_name = input("name: ")
    makea_qr(tmp_code, tmp_name)
    qr_path  = join(dirname(__file__), QRC_DIREC + tmp_name + FILE_TYPE)
    out_path = join(dirname(__file__) + '\\' + tmp_name + FILE_TYPE)
    post_path= join(dirname(__file__), POS_DIREC)
    paste_qr(post_path, qr_path, out_path)