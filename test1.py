import io
import time
'''
wand是基于ctypes的python简单ImageMagick绑定， 支持2.6、2.7、3.3+和Pypy。
目前，并非全部 magickwand api的功能已经在wand中实现了。
ImageMagick to create, edit, compose, or convert digital images. 
It runs on Linux, Windows, Mac Os X, iOS, Android OS, and others.
'''

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
    f.close()


run_convert("test.pdf", 2)
