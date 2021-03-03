import qrcode
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    box_size=10,
    border=4
)

imagewidth, imageheight = (290, 290)
qr.add_data('Some data')
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")

I1 = ImageDraw.Draw(img)
myFont = ImageFont.truetype("sonic.ttf", 50)
w, h = I1.textsize("zephyr")
I1.text(((imagewidth-w)/2, 250), 'zephyr', font= myFont, fill = "black")


img.save("hi.png", "PNG")
