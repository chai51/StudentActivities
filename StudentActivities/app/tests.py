import qrcode 
from PIL import Image, ImageFont, ImageDraw

# Create your tests here.
staticResUrl = ''

# 生成二维码海报
def createQRCodeEx(bk, name, content, url, savePath):
    fontSize = 50
    font = ImageFont.truetype('static/handBook.ttf', fontSize)
    font2 = ImageFont.truetype('static/pudding.ttf', fontSize)

    image = Image.open(bk).convert('RGBA')
    draw = ImageDraw.Draw(image)
    width, height = image.size

    y = height * 0.7
    draw.text((width*0.5 - len(name)*fontSize*0.5 , y), name, fill=(255,0,0,255), font=font)
    y = y + fontSize * 1.1
    draw.text((width*0.5 - len(content)*fontSize*0.5 , y), content, fill=(0,0,0,255), font=font2)

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    qr_code = qr.make_image()
    qr_code2 = qr_code.resize((128, 128))
    
    x = int(width*0.5 - qr_code2.size[0]*0.5)
    y = int(y + fontSize * 1.1)
    image.paste(qr_code2, box=(x,y))
    #draw.bitmap((x,y), qr_code)
    image.save(savePath, "png")

def createQRCode(url, savePath):
    image = qr_code = qrcode.make(url)
    image.save(savePath)

def convertImgFmt(inFile, outFile):
    Image.open(inFile).save(outFile)

def convertPath(inPath):
    path = "/var/nginx/html"
    pathPrefix = ''
    if path in inPath:
        return pathPrefix + inPath[len(path):]
    return inPath