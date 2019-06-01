import qrcode 
from PIL import Image, ImageFont, ImageDraw
import time
import base64
import hmac

# Create your tests here.
staticResUrl = ''

# 生成二维码海报
def createQRCodeEx(bk, name, content, url, savePath, description):
    fontSize = 50
    fontSize2 = int(fontSize/2)
    font = ImageFont.truetype('static/handBook.ttf', fontSize)
    font2 = ImageFont.truetype('static/pudding.ttf', fontSize2)

    image = Image.open(bk).convert('RGBA')
    draw = ImageDraw.Draw(image)
    width, height = image.size

    x = width*0.5 - (len(name)*fontSize*0.5 + len(content)*fontSize2*0.5)
    y = height * 0.7
    draw.text((x, y), name, fill=(153,0,153,255), font=font)
    x = x + len(name)*fontSize
    y = y + fontSize2
    draw.text((x, y), content, fill=(255,255,255,255), font=font2)

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    qr_code = qr.make_image()
    qr_code2 = qr_code.resize((128, 128))
    
    x = int(width*0.5 - qr_code2.size[0]*0.5)
    y = int(y + fontSize)
    image.paste(qr_code2, box=(x,y))

    x = width*0.5 - (len(description)*fontSize2*0.5)
    y = y + 128 + 20
    draw.text((x,y), description, fill=(0,190,166,255), font=font2)
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

def createToken(user):
    timestamp = str(time.time())
    sha1 = hmac.new(user.encode("utf-8"), timestamp.encode("utf-8"), 'sha1').hexdigest()
    token = timestamp + ':' + sha1
    return base64.urlsafe_b64encode(token.encode("utf-8")).decode("utf-8")