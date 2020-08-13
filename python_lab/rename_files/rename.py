import os

mypath = "D:\\Photos\\2013\\201310"
#mypath="D:\\Pics\\2011\201101"
#mypath = "C:\\Users\\quantboy\\pics"
onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
for f in onlyfiles:
    if f[0] == 'p' or f[0] == 'm':
        orig_name = mypath + "\\" + f
        new_name = mypath + "\\" + f[1:]
        if os.path.isfile(new_name):
            print('%s exists, remove %s' % (new_name, orig_name))
            os.remove(orig_name)
        else:
            print('rename %s to %s' % (orig_name, new_name))
            os.rename(orig_name, new_name)
    if f[0:3] == 'IMG':
        orig_name = mypath + "\\" + f
        new_name = mypath + "\\" + f[4:]
        print('rename %s to %s' % (orig_name, new_name))
        os.rename(orig_name, new_name)
    if f[0:4] == 'VID_':
        orig_name = mypath + "\\" + f
        new_name = mypath + "\\" + f[4:]
        print('rename %s to %s' % (orig_name, new_name))
        os.rename(orig_name, new_name)

