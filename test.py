# coding=utf-8

from PIL import Image, ImageDraw, ImageFont
import pdfE
'''
image = Image.new(mode='RGBA', size=(200, 200))
draw_table = ImageDraw.Draw(im=image)
draw_table.text(xy=(0, 0), text=u'仰起脸笑得像满月', fill=(0, 0, 0, 30), font=ImageFont.truetype('/System/Library/Fonts/PingFang.ttc', 50))
 
image.show()  # 直接显示图片
image.save('test满月.png', 'PNG')  # 保存在当前路径下，格式为PNG
image.close()
'''

pdfE.run_convert_all("test.pdf")
