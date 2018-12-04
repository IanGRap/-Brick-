import os
import sys
import shutil
from google_images_download import google_images_download   #importing the retrival library
from PIL import Image
from random import randint

def generate_initial_population(query, population_size, verbose):
    # ---- Function Variables ---- #
    dirName = "population"
    path = "downloads"
    population_count = 0

    # ------------- Remove Past Images ------------------------------------------------------------ #
    if os.path.exists(path):
        print("Removeing Past Downloads...")
        shutil.rmtree(path + '/', ignore_errors=False, onerror=None)
    if os.path.exists(dirName):
        print("Removeing Past Population...")
        shutil.rmtree(dirName + '/', ignore_errors=False, onerror=None)

    # ------------- Get Images From Internet-------------------------------------------------------------------- #
    response = google_images_download.googleimagesdownload()   #class instantiation

    arguments = {"keywords":query,"limit":population_size+10,"print_urls":verbose, "format":"jpg", "usage_rights":"labeled-for-nocommercial-reuse", "no_directory":True}   #creating list of arguments
    paths = response.download(arguments)   #passing the arguments to the function
    print(paths)   #printing absolute paths of the downloaded images

    # ------------- Make Folder for Population ----------------------------------------------------#
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory " , dirName ,  " Created ")
    else:    
        print("Directory " , dirName ,  " already exists")

    # -------------- Tidy Up Images ----------------------------------------------------------------#

    for filename in os.listdir(path + '/'):
        print("Cleaning up " + filename)
        try:
            src_image = Image.open(path + '/' + filename)
            if src_image and population_count < population_size:
                new_image = src_image.resize((1024,1024), resample=0)
                new_image.save(dirName + '/' + str(population_count) + '.png')
                population_count += 1
        except:
            print("Cleanup Failed!")
            pass

    if population_count is population_size:
        print("\nSuccessfully Generated Initial Population")
    elif population_count > 0:
        print("\nFailed To Generate Some Members Of Initial Population")
    else:
        print("\nFailed To Generate Initial Population")
    print("Population Size: " + str(population_count))

# -- MAIN -- #
# ------------- Proccess User input ----------------------------------------------------------- #
 
query = ""
for i in range(1, len(sys.argv)-1):
    query += sys.argv[i] + " texture,"
query += sys.argv[len(sys.argv)-1] + " texture"
population_size = 20
verbose = True

generate_initial_population(query, population_size, verbose)


# --------------- Display Using Tkinter --------------------------------------------------------#

# --------------- Selection --------------------------------------------------------------------#

"""
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
"""
