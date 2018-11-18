import os
import sys
import time
import requests
import subprocess


def get_chapter_contents(page_url, link_page):
    chapter_link = page_url + '/' + link_page
    r = requests.get(chapter_link)
    data = r.content.decode('gbk')
    content =  get_content(data)
    return content



def get_chapter_links(toc):
    links = {}
    chapter_titles = {}
    next_chapter_start_idx = 0
    chapter_title = ''
    link_page = ''
    chapter = 1
    while(True):
        next_chapter_start_idx = toc.find('a href="', next_chapter_start_idx+1)
        if next_chapter_start_idx>0:
            next_chapter_end_idx = toc.find('html"', next_chapter_start_idx)
            if next_chapter_end_idx>0:
                link_page = toc[next_chapter_start_idx+8:next_chapter_end_idx+4]
                links[chapter] = link_page
                chapter_title_start_idx = toc.find('>', next_chapter_end_idx)
                chapter_title_end_idx = toc.find('<', next_chapter_end_idx)
                if chapter_title_start_idx>0 and chapter_title_end_idx>0:
                    chapter_title = toc[chapter_title_start_idx+1:chapter_title_end_idx]
                    chapter_titles[chapter] = chapter_title
                    print("%s %s" % (chapter, chapter_title))
            chapter = chapter + 1
        else:
            break
    return( links, chapter_titles )



def get_table_of_contents(data):
    toc = ''
    toc_start_idx = data.find('id="list">')
    if toc_start_idx>0:
        toc_end_idx = data.find('</div>', toc_start_idx)
        if toc_end_idx>0:
            toc = data[toc_start_idx+8:toc_end_idx-1]

    return toc



# find H1
def get_title(data):
    title = ''
    heading_start_idx = data.find('h1')
    if heading_start_idx>0:
        heading_end_idx = data.find('/h1', heading_start_idx+1)
        if heading_end_idx>0:
            title = data[heading_start_idx+4:heading_end_idx-1]
    return title


# find content
def get_content(data):
    content = ''
    content_start_idx = data.find('<div id="content">')
    if content_start_idx>0:
        content_end_idx = data.find('</div>', content_start_idx+1)
        if content_end_idx>0:
            content = data[content_start_idx+18:content_end_idx]

    content = content.replace( '&nbsp;', ' ')
    content = content.replace( '<br /><br />', '<p><p>\n')
    return content


def get_book_property(data, prop):
    value = ''
    prop_start_idx = data.find(prop)
    if prop_start_idx>0:
        prop_end_idx = data.find('/>', prop_start_idx+1)
        if prop_end_idx>0:
            value = data[prop_start_idx+len(prop):prop_end_idx-1]

    return value




book_num = 1192
folder_num = book_num // 1000
page_url = 'http://www.5du5.net/book/%s/%s' % (folder_num, book_num)

r = requests.get(page_url)
data = r.content.decode('gbk')
title = get_book_property(data, 'og:novel:book_name" content="')
author = get_book_property(data, 'og:novel:author" content="')
cover = get_book_property(data, 'og:image" content="')

get_cover_jpg_command = "~/anaconda3/bin/curl %s > cover.jpg" % cover
os.system( get_cover_jpg_command )

toc =  get_table_of_contents(data)
print(title)
print(author)
(links, chapter_titles) = get_chapter_links(toc)
print(len(links))
print(len(chapter_titles))

output_name = "c%s.html" % book_num
mobi_name = "c%s.mobi" % book_num
f = open(output_name, 'w')
f.write('<html>\n')
f.write('\t<body>\n')
for idx in range(5200,len(links)+1):
    #if idx>4000:
    #    continue
    print ("%s/%s %s %s" % (idx, len(links), links[idx], chapter_titles[idx]) )
    chapter_contents = get_chapter_contents(page_url, links[idx])
    chapter_title = chapter_titles[idx]

    utitle = chapter_title.encode('utf-8')
    ucontents = chapter_contents.encode('utf-8')

    f.write('\t\t<h2 class="chapter">%s</h2>\n' % utitle)
    f.write('\t\t<p>%s<p>\n' % ucontents)
    f.write('\n')
f.write('\t</body>\n')
f.write('</html>\n')

print("/usr/bin/ebook-convert %s %s --title %s --level1-toc h2 --verbose --insert-blank-line --cover cover.jpg --embed-all-fonts --chapter-mark both --mobi-toc-at-start --toc-title TOC --max-toc-links 9999 --authors %s" % (output_name, mobi_name, title, author ) )



