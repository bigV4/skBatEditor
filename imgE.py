# coding:utf-8
from PIL import Image, ImageDraw, ImageFont
import shutil
import os
import sys
import zipfile
import re

def unzip_file(zip_src, dst_dir):
    r = zipfile.is_zipfile(zip_src)
    if r:     
        fz = zipfile.ZipFile(zip_src, 'r')
        for file in fz.namelist():
            fz.extract(file, dst_dir)       
    else:
        print('This is not zip')

def add_text_to_image(image, text, font_size=24, sparse=1):
    #font = ImageFont.truetype('C:\Windows\Fonts\STXINGKA.TTF', font_size)
    font = ImageFont.truetype('/System/Library/Fonts/PingFang.ttc', font_size)
    # 添加背景
    new_img = Image.new('RGBA', (image.size[0] * 3, image.size[1] * 3), (0, 0, 0, 0))
    #RGBA意思是红色，绿色，蓝色，Alpha的色彩空间，Alpha指透明度。JPG不支持透明度，所以要么丢弃Alpha,要么保存为.png
    new_img.paste(image, image.size)
    # 添加水印
    font_len = len(text)
    str_len = font_len-len(''.join(re.findall(r'[a-z0-9]', text)))*0.5-len(''.join(re.findall(r'[A-Z]', text)))*0.35
    print("font_len ",font_len )
    rgba_image = new_img.convert('RGBA')
    text_overlay = Image.new('RGBA', rgba_image.size, (255, 255, 255, 0))
    image_draw = ImageDraw.Draw(text_overlay)
    for i in range(0, rgba_image.size[0], int(font_size*str_len*sparse)):
        for j in range(0, rgba_image.size[1], int(font_size*sparse)):
            image_draw.text((i, j), text, font=font, fill=(0, 0, 0, 30))
    text_overlay = text_overlay.rotate(-45)
    image_with_text = Image.alpha_composite(rgba_image, text_overlay)
    # 裁切图片
    image_with_text = image_with_text.crop((image.size[0], image.size[1], image.size[0] * 2, image.size[1] * 2))
    return image_with_text

def add_text_to_docximage(image, text, source='test.docx', target='temp/'):
    assert not os.path.isabs(source)
    target = os.path.join(target, os.path.dirname(source))
    try:# create the folders if not already exists
        os.makedirs(target)
    except FileExistsError as e:
        print(e)
    try:# adding exception handling
        shutil.copy(source, target)
    except IOError as e:
        print("Unable to copy file. %s" % e)
    except:
        print("Unexpected error:", sys.exc_info())
    tempdocxpath = target+"/"+source
    tempzippath = target+"/"+source+".zip"
    tempunzippath = target+"/"+source.replace(".","_")
    os.rename(tempdocxpath, tempzippath)
    unzip_file(tempzippath, tempunzippath)
    names = os.listdir(tempunzippath+"/word/media")    #这将返回一个所有文件名的列表
    print(names)
    for imgpath in names:
        img = Image.open(tempunzippath+"/word/media/"+imgpath)
        im_after = add_text_to_image(img, text)
        try:
            im_after.save(tempunzippath+"/word/media/"+imgpath)
        except OSError as e:
            print(e)
            im_after = im_after.convert('RGB')
            im_after.save(tempunzippath+"/word/media/"+imgpath)

if __name__ == '__main__':
    text = u'测试使用'
    text=u"瑞数信息RIVERSECURITY"
    #text=u"瑞数信息科技有小公司"
    img = Image.open("test.jpg")
    im_after = add_text_to_image(img, text)
    im_after.save(u'dest/测试使用.png')
    add_text_to_docximage(img, text)