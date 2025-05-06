import os
import time
import src.core.setcore as core
import qrcode
def gen_qrcode(url):
    qr = qrcode.QRCode(5, error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(url)
    qr.make()
    im = qr.make_image()
    time.sleep(1)
    qr_img_path = os.path.join(core.userconfigpath, "reports/qrcode_attack.png")
    if os.path.isfile(qr_img_path):
        os.remove(qr_img_path)
    im.save(qr_img_path, format='png')
    core.print_status("QRCode has been generated under {0}".format(qr_img_path))