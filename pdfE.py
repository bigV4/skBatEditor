# pip3 install PyPDF2 -i https://pypi.doubanio.com/simple/ --trusted-host pypi.doubanio.com
# pip3 install Wand -i https://pypi.doubanio.com/simple/ --trusted-host pypi.doubanio.com
# -*- coding: utf-8 -*-
import io
import time
'''
wand是基于ctypes的python简单ImageMagick绑定， 支持2.6、2.7、3.3+和Pypy。
目前，并非全部 magickwand api的功能已经在wand中实现了。
'''
from wand.image import Image
from wand.color import Color
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
import sys
import os
import datetime

memo = {}


def get_pdf_reader(filename):
    reader = memo.get(filename, None)
    if reader is None:
        # 不解密可能会报错：PyPDF2.utils.PdfReadError: File has not been decrypted
        # 将 PDF文件读取出来，转换成 PdfFileReader
        reader = PdfFileReader(filename, strict=False)
        memo[filename] = reader
    return reader


def get_pdf_reader2(filename):
    f = open(filename, "rb")
    reader = memo.get(filename)
    if reader is None:
        # 不解密可能会报错：PyPDF2.utils.PdfReadError: File has not been decrypted
        reader = PdfFileReader(f)  # 将 PDF文件读取出来，转换成 PdfFileReader
        memo[filename] = reader
    return reader, f


def get_num_pages(filename, pdfile):
    """
    获取文件总页码
    :param pdfile: PDF文件PdfFileReader
    :return:
    """
    if pdfile.isEncrypted:
        pdfile.decrypt('')
    page_num = pdfile.getNumPages()
    print("PDF file %s has %r pages" % (filename, page_num))
    return page_num


def run_convert(filename, page, res=120):
    '''把pdf指定页码转化为图片'''
    pdfile, f = get_pdf_reader(filename), open(filename, "rb")
    # pdfile,f = get_pdf_reader2(filename)
    if page <= pdfile.getNumPages():
        idx = page + 1
        temp_time = time.time() * 1000
        # 由于每次转换的时候都需要重新将整个PDF载入内存，所以这里使用内存缓存
        pageobj = pdfile.getPage(page)
        print(type(pageobj))
        dst_pdf = PdfFileWriter()
        dst_pdf.addPage(pageobj)

        pdf_bytes = io.BytesIO()
        dst_pdf.write(pdf_bytes)
        pdf_bytes.seek(0)
        # resolution是分辨率
        img = Image(file=pdf_bytes, resolution=res)
        img.format = 'png'
        img.compression_quality = 90
        img.background_color = Color("white")
        # 保存图片
        img_path = 'dest/%s_pg%d.png' % (filename[:filename.rindex('.')], idx)
        img.save(filename=img_path)
        img.destroy()
        img, pdf_bytes, dst_pdf = None, None, None
        print('convert page %d cost time %dms' %
              (idx, (time.time() * 1000 - temp_time)))
    else:
        print("pg%r list index out of range" % page)
    f.close()


def run_convert_all(filename, destpath="./dest/", res=120):
    '''把pdf所有页面转化为图片'''
    # 由于每次转换的时候都需要重新将整个PDF载入内存，所以这里使用内存缓存
    pdfile, f = get_pdf_reader(filename), open(filename, "rb")
    # pdfile,f = get_pdf_reader2(filename)
    for i in range(0, pdfile.getNumPages()):
        temp_time = time.time() * 1000
        pageobj = pdfile.getPage(i)
        dst_pdf = PdfFileWriter()
        dst_pdf.addPage(pageobj)

        pdf_bytes = io.BytesIO()
        dst_pdf.write(pdf_bytes)
        pdf_bytes.seek(0)
        # resolution是分辨率
        img = Image(file=pdf_bytes, resolution=res)
        img.format = 'png'
        img.compression_quality = 90
        img.background_color = Color("white")
        # 保存图片
        img_path = '%s_pg%d.png' % (filename[:filename.rindex('.')], i+1)
        img_path = destpath + img_path
        img.save(filename=img_path)
        img.destroy()
        img, pdf_bytes, dst_pdf = None, None, None
        print('convert page %d cost time %dms' %
              (i+1, (time.time() * 1000 - temp_time)))
    f.close()


def create_watermark(content):
    """制作水印pdf文件"""
    # 默认大小为21cm*29.7cm
    file_name = "mark.pdf"
    c = canvas.Canvas(file_name, pagesize=(30*cm, 30*cm))
    # 移动坐标原点(坐标系左下为(0,0))
    c.translate(10*cm, 5*cm)
    # 设置字体‘C:\Windows\Fonts’
    c.setFont("Helvetica", 36)
    # 指定描边的颜色
    c.setStrokeColorRGB(0, 1, 0)
    # 指定填充颜色
    c.setFillColorRGB(0, 1, 0)
    # 旋转45度,坐标系被旋转
    c.rotate(30)
    # 指定填充颜色
    c.setFillColorRGB(0, 0, 0, 0.1)
    # 设置透明度,1为不透明
    # c.setFillAlpha(0.1)
    # 画几个文本,注意坐标系旋转的影响
    for i in range(5):
        for j in range(10):
            a = 10*(i-1)
            b = 5*(j-2)
            c.drawString(a*cm, b*cm, content)
            c.setFillAlpha(0.1)
    # 关闭并保存pdf文件
    c.save()
    return file_name


def add_watermark(pdf_file_in, pdf_file_out, content):
    """把水印添加到pdf中"""
    pdf_file_mark = create_watermark(content)
    pdf_output = PdfFileWriter()
    input_stream = open(pdf_file_in, 'rb')
    pdf_input = PdfFileReader(input_stream, strict=False)

    # 获取PDF文件的页数
    pagenum = pdf_input.getNumPages()

    # 读入水印pdf文件
    pdf_watermark = PdfFileReader(open(pdf_file_mark, 'rb'), strict=False)
    # 给每一页打水印
    for i in range(pagenum):
        page = pdf_input.getPage(i)
        page.mergePage(pdf_watermark.getPage(0))
        page.compressContentStreams()  # 压缩内容
        pdf_output.addPage(page)
    pdf_output.write(open(pdf_file_out, 'wb'))


def split_pdf(filename, result, start=0, end=None):
    """从filename中提取[start,end)之间的页码内容保存为result"""
    # 切割出的PDF文件不含start页，含end页，即如想获得2-5页，start=1，end=5
    # 打开原始 pdf 文件
    pdf_src = PdfFileReader(filename)
    if end is None:
        # 获取页数
        end = pdf_src.getNumPages()
    with open(result, "wb") as fp:
        # 创建空白pdf文件
        pdf = PdfFileWriter()
        # 提取页面内容，写入空白文件
        for num in range(start, end):
            pdf.addPage(pdf_src.getPage(num))
        # 写入结果pdf
        pdf.write(fp)
