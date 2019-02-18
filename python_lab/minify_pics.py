from PIL import Image
import os
import sys
import ast

# import photos from specified folder
# 
# minify_pics folder size
#

def get_file_date_time(exif_data):
    try:
        dtime = exif_data[36867]
        # 2017:05:27 19:05:14
        dtime = dtime.replace(':', '')
        dtime = dtime.replace(' ', '_')
        return dtime
    except:
        return ""


def resize_image_if_larger_than_1600(img):
    new_img = img
    imgsize = img.size
    if imgsize[0] > 1600 or imgsize[1] > 1600:
        r = imgsize[0] / 1600.0
        if imgsize[1] > imgsize[0]:
            r = imgsize[1] / 1600.0
        print('ratio %d' % (r))
        # 2000 / 1600 = 1.5625
        # to get 2000 to 1600 => w/1.5625 
        new_width = int(imgsize[0] / r)
        new_height = int(imgsize[1] / r)

        msg = '%d, %d' % (new_width, new_height)
        print(msg)
        new_img = img.resize((new_width, new_height)) 

    return new_img


#def get_new_file_name(exif_data):
#    newname = ''
#    if 37510 in exif_data:
#        user_content = exif_data[37510]
#        user_dict = ast.literal_eval(user_content)
#        file_type = user_dict['ext']
#        newname = 'p' + dtime + '.jpg'
#    else:
#        newname = 'p' + dtime + '.jpg'
#
#    return newname



searchfolder = sys.argv[1]
allfiles = os.listdir(searchfolder)
for f in allfiles:
    if not f.endswith('jpg') and not f.endswith('JPG'):
        continue
    
    img_file = searchfolder + '/' + f
    img = Image.open(img_file)
    exif_data = img._getexif()
    #print(exif_data)
    #print(img.mode)

    dtime = get_file_date_time(exif_data)
    if dtime == "":
        continue
    newname = 'p' + dtime + '.jpg'
    print(newname)

    new_img = resize_image_if_larger_than_1600(img)
    #new_img = new_img.convert('L')

    new_img_file = '/tmp/' + newname
    print('Saving ' + new_img_file)
    new_img.save(new_img_file)


    




