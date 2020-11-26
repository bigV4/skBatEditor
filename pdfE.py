#pip3 install PyPDF2 -i https://pypi.doubanio.com/simple/ --trusted-host pypi.doubanio.com 
#pip3 install Wand -i https://pypi.doubanio.com/simple/ --trusted-host pypi.doubanio.com 
# -*- coding: utf-8 -*-
import io
import time

from wand.image import Image
from wand.color import Color
from PyPDF2 import PdfFileReader, PdfFileWriter

memo = {}


def getPdfReader(filename):
    reader = memo.get(filename, None)#
    if reader is None:
        # 不解密可能会报错：PyPDF2.utils.PdfReadError: File has not been decrypted
        reader = PdfFileReader(filename, strict=False)#将 PDF文件读取出来，转换成 PdfFileReader
        memo[filename] = reader
    return reader

def getPdfReader2(filename):
    f = open(filename, "rb")
    reader = memo.get(filename)#
    if reader is None:
        # 不解密可能会报错：PyPDF2.utils.PdfReadError: File has not been decrypted
        reader = PdfFileReader(f)#将 PDF文件读取出来，转换成 PdfFileReader
        memo[filename] = reader
    return reader,f

def get_num_pages(filename,pdfile):
    """
    获取文件总页码
    :param pdfile: PDF文件PdfFileReader
    :return:
    """
    if pdfile.isEncrypted:
        pdfile.decrypt('')
    page_num = pdfile.getNumPages()
    print("PDF file %s has %r pages"%(filename,page_num))
    return page_num

def _run_convert(filename, page, res=120):
    #pdfile = getPdfReader(filename)
    pdfile,f = getPdfReader2(filename)
    if page <= get_num_pages(filename,pdfile):
        idx = page + 1
        temp_time = time.time() * 1000
        # 由于每次转换的时候都需要重新将整个PDF载入内存，所以这里使用内存缓存
        pageObj = pdfile.getPage(page)
        dst_pdf = PdfFileWriter()
        dst_pdf.addPage(pageObj)

        pdf_bytes = io.BytesIO()
        dst_pdf.write(pdf_bytes)
        pdf_bytes.seek(0)

        img = Image(file=pdf_bytes, resolution=res)
        img.format = 'png'
        img.compression_quality = 90
        img.background_color = Color("white")
        # 保存图片
        img_path = '%s_pg%d.png' % (filename[:filename.rindex('.')], idx)
        img.save(filename=img_path)
        img.destroy()
        img,pdf_bytes,dst_pdf = None,None,None
        print('convert page %d cost time %dms' % (idx, (time.time() * 1000 - temp_time)))
    else:
        print("pg%r list index out of range"%page)
    f.close()

def _run_convert_all(filename, res=120):
    # 由于每次转换的时候都需要重新将整个PDF载入内存，所以这里使用内存缓存
    #pdfile = getPdfReader(filename)
    pdfile,f = getPdfReader2(filename)
    for i in range(0,get_num_pages(filename,pdfile)):
        temp_time = time.time() * 1000
        pageObj = pdfile.getPage(i)
        dst_pdf = PdfFileWriter()
        dst_pdf.addPage(pageObj)

        pdf_bytes = io.BytesIO()
        dst_pdf.write(pdf_bytes)
        pdf_bytes.seek(0)

        img = Image(file=pdf_bytes, resolution=res)
        img.format = 'png'
        img.compression_quality = 90
        img.background_color = Color("white")
        # 保存图片
        img_path = '%s_pg%d.png' % (filename[:filename.rindex('.')], i+1)
        img.save(filename=img_path)
        img.destroy()
        img,pdf_bytes,dst_pdf = None,None,None
        print('convert page %d cost time %dms' % (i+1, (time.time() * 1000 - temp_time)))
    f.close()

if __name__ == '__main__':
    _run_convert('demo.pdf', 120)
    _run_convert_all('demo.pdf')
