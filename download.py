import os
import sys
import shutil
from google_images_download import google_images_download   #importing the retrival library
from PIL import Image
from random import randint

# ------------- Proccess User input ----------------------------------------------------------- #
 
query = ""
for i in range(1, len(sys.argv)-1):
    query += sys.argv[i] + " texture,"
query += sys.argv[len(sys.argv)-1] + " texture"
population_size = 20
verbose = True

# ------------- Remove Past Images ------------------------------------------------------------ #
if os.path.exists("downloads"):
    shutil.rmtree('downloads/', ignore_errors=False, onerror=None)
if os.path.exists("population"):
    shutil.rmtree('population/', ignore_errors=False, onerror=None)

# ------------- Get Images -------------------------------------------------------------------- #
response = google_images_download.googleimagesdownload()   #class instantiation

arguments = {"keywords":query,"limit":population_size+10,"print_urls":verbose, "format":"jpg", "usage_rights":"labeled-for-nocommercial-reuse", "no_directory":True}   #creating list of arguments
paths = response.download(arguments)   #passing the arguments to the function
print(paths)   #printing absolute paths of the downloaded images

# ------------- Make Folder for Population ----------------------------------------------------#
dirName = "population"
if not os.path.exists(dirName):
    os.mkdir(dirName)
    print("Directory " , dirName ,  " Created ")
else:    
    print("Directory " , dirName ,  " already exists")

# -------------- Tidy Up Images ----------------------------------------------------------------#
path = 'downloads/'
count = 0

for filename in os.listdir(path):
    print(filename)
    try:
        src_image = Image.open(path + filename)
        if src_image and count < population_size:
            new_image = src_image.resize((1024,1024), resample=0)
            new_image.save(dirName + '/' + str(count) + '.png')
            count += 1
    except:
        pass

population_size = count
print("Population Size: " + str(population_size) + "\n")

# --------------- Display Using Tkinter --------------------------------------------------------#

# --------------- Selection --------------------------------------------------------------------#

# --------------- Crossover --------------------------------------------------------------------#
imgs = []
for filename in os.listdir(dirName):
    imgs.append(Image.open(dirName + "/" + filename))
new_image = imgs[0]
for i in range(1, population_size-1):
    print("merging images " + str(i) + " and " + str(i+1))
    try:
        new_image = Image.blend(imgs[i],imgs[i+1],0.5)
    except:
        pass

new_image.save("new_image.png");
new_image.show()

