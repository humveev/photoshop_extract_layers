"""
22.01.2019 Robin Grob
- Created Skriptes

23.01.2019 Robin Grob
- Fixed a Bug which aborded the export of Layers
"""



"""
TODO:
cmd:
    pip install psd-tools2
    pip install Pillow
"""
#Imports
import os
import sys
import shutil
import subprocess
import Tkinter, tkFileDialog, tkMessageBox
    

#Fenster initialisieren
root = Tkinter.Tk()
root.withdraw()

try:
    from psd_tools import PSDImage
    from PIL import Image
except ImportError:
    tkMessageBox.showerror("Fatal Error!",
"""Couldn't find PSD-Tools2! Please follow the following Steps:\n\r
1. Open Commandline (In startmenu type cmd -> Run as Admin)\n\r
2. Type "pip install psd-tools2" and hit Enter\n\r
3. Type "pip install Pillow" and hit Enter\n\r
-> After these steps the script should work""")
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
    print file_name
except:
    tkMessageBox.showerror("Error","Wrong File! \nSELECT .PSD Try again! \n :) (r)Robin Grob")
    print("Wrong File! Try again! \n :) (r)Robin Grob")
    sys.exit()

new_dir_name = os.path.splitext(file_name)[0]
print new_dir_name

if os.path.exists(new_dir_name) is True:
    shutil.rmtree(new_dir_name)
    
os.mkdir(new_dir_name)

os.chdir(new_dir_name)


psd.print_tree()
print "####################"
print psd.layers
print "####################"
print len(list(psd.descendants()))
print "####################"
print list(psd.descendants())
print "---------------------"

image_size = psd.as_PIL().size
print image_size


for i in list(psd.descendants()):

    try:
        img = Image.new('RGBA',image_size,0)
        temp = i.as_PIL()
        temp_bbox = i.bbox
        name = 'temp_'+str(list(psd.descendants()).index(i))+'.png'
        img.paste(temp,temp_bbox)
        temp.save(name)
        img.save('img_'+name)
        file = open('whole list with bbox.txt',"a")
        file.write(name + ': ' + str(i.bbox) + '\n')
    except AttributeError:
        continue

file.close()
subprocess.Popen(r'explorer /select,'+str(os.getcwd()))
sys.exit()
