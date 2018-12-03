import os
import sys
import requests
import string
import time
from fpdf import FPDF
from datetime import datetime
from bs4 import BeautifulSoup
import shutil


def get_html_contents(base_html):
    contents = ""
    with open(base_html) as cfile:
        contents = cfile.read()
    return contents


def get_page_links(html):    

    marker = 'lstImages.push("' 
    marker_end = '")'
    marker_len = len(marker)

    # get the list of images
    idx = 0
    jpgs = []
    while idx>-1:
        print('finding %s' % idx)
        idx = html.find(marker,idx)
        if idx == -1:
            break
        endidx = 0
        endidx = html.find(marker_end, idx)
        if endidx == -1:
            break
        pagejpg = html[idx+marker_len:endidx]
        print(pagejpg)
        jpgs.append(pagejpg)
        idx = idx+1

    return jpgs


def download_jpg(jpg, target_filename):
    response = requests.get(jpg, stream=True)
    with open(target_filename, 'wb') as outfile:
        shutil.copyfileobj(response.raw, outfile)
    del response


def download_links_to_jpgs(jpgs):
    jpg_filenames = []
    for i, jpg in enumerate(jpgs):
        jpg_filename = format('/tmp/j%s.jpg' % i)
        download_jpg(jpg, jpg_filename)
        jpg_filenames.append(jpg_filename)
    return jpg_filenames


def save_jpgs_to_pdf(jpg_filenames, target_pdf):
    pdf = FPDF()
    for jpg in jpg_filenames:
        pdf.add_page()
        pdf.image(jpg)
    pdf.output(target_pdf, "F")


def clear_all_tmp_files():
    os.system('rm -rf /tmp/*jpg')
    os.system('rm -rf /tmp/*cbz')



def save_jpgs_to_cbz(target_cbz):
    cmd = format('zip %s /tmp/*.jpg' % target_cbz)
    os.system(cmd)


if len(sys.argv)<2: 
    print('comix.py comic.html target.cbz')
    exit(-1)
    
comic_html = sys.argv[1]
target_cbz = sys.argv[2]

clear_all_tmp_files()
contents = get_html_contents(comic_html) 
jpgs = get_page_links(contents)
jpg_filenames = download_links_to_jpgs(jpgs)
save_jpgs_to_cbz(target_cbz)
