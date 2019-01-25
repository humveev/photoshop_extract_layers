"""
22.01.2019 Robin Grob (https://github.com/humveev)
- Created Skriptes

23.01.2019 Robin Grob (https://github.com/humveev)
- Fixed a Bug which aborded the export of Layers

25.01.2019Robin Grob (https://github.com/humveev)
- Fixed installation of modules guide
- Added Support for psd-tools2 v1.8
"""



"""
TODO:
run cmd as admin:
    python -m pip install psd-tools2
    python -m pip install psd-tools2 --upgrade
    python -m pip install Pillow
    python -m pip install Pillow --upgrade
"""


#Imports
import os
import sys
import shutil
import subprocess
import Tkinter, tkFileDialog, tkMessageBox
    

#Initialize popups
root = Tkinter.Tk()
root.withdraw()

try:
    from psd_tools import PSDImage
    from PIL import Image
except ImportError:
    try:
        from psd_tools2 import PSDImage
        from PIL import Image
    except ImportError:
        tkMessageBox.showerror("Fatal Error!",
"""Couldn't find PSD-Tools2 or PSD-Tools2 outdated! Please follow the following Steps:\n\r
1. Open Commandline (In startmenu type cmd -> Run as Admin)\n\r
2. Type "python -m pip install psd-tools2" and hit Enter\n\r
3. Type "Python -m pip install psd-tools2 --upgrade" and hit Enter\n\r
4. Type "python -m pip install Pillow" and hit Enter\n\r
5. Type "python -m pip install Pillow --upgrade" and hit Enter\n\r
-> After these steps the script should work\n\r
Robin Grob https://github.com/humveev""")
        sys.exit()


file_path = tkFileDialog.askopenfilename()

print file_path
if file_path == "":
    sys.exit()
file_name = os.path.basename(os.path.normpath(file_path))
print file_name
if file_name == "":
    sys.exit()
print os.path.splitext(file_name)[1]

if os.path.splitext(file_name)[1] == "":
    sys.exit()

try:
    psd = PSDImage.load(file_name)
except:
    try:
        psd = PSDImage.open(file_name)
    except:
        tkMessageBox.showerror("Error","Wrong File! \nSELECT .PSD Try again! \n :) (r)Robin Grob")
        print("Wrong File! Try again! \n :) (r)Robin Grob (https://github.com/humveev)")
        sys.exit()
print file_name

new_dir_name = os.path.splitext(file_name)[0]
print new_dir_name

if os.path.exists(new_dir_name) is True:
    shutil.rmtree(new_dir_name)
    
os.mkdir(new_dir_name)

os.chdir(new_dir_name)


print "####################"
#print psd
print "####################"
print len(list(psd.descendants()))
print "####################"
print list(psd.descendants())
print "---------------------"

try:
    image_size=psd.as_PIL().size
except:
    image_size = psd.topil().size

print image_size

file = open('whole list with bbox.txt',"a")

for i in list(psd.descendants()):
    print i
    try:
        img = Image.new('RGBA',image_size,0)
        try:
            temp = i.as_PIL()
        except:
            temp = i.compose()
        temp_bbox = i.bbox
        print temp_bbox
        name = 'temp_'+str(list(psd.descendants()).index(i))+'.png'
        try:
            img.paste(temp,temp_bbox)
        except:
            name = 'error'+str(list(psd.descendants()).index(i))+'.png'
            continue
        temp.save(name)
        img.save('img_'+name)
        file.write(name + ': ' + str(i.bbox) + '\n')
    except AttributeError:
        continue

file.close()
print os.getcwd()
subprocess.Popen(r'explorer /select,'+str(os.getcwd())+'\\temp_0.png')
sys.exit()
