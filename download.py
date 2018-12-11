import os
import sys
import shutil
from google_images_download import google_images_download   #importing the retrival library
from PIL import Image
from random import randint, random, shuffle

def generate_initial_population(query, num_queries, population_size, verbose):
    # ---- Function Variables ---- #
    dirName = "population"
    path = "downloads"
    population_count = 0
    population = []
    images_of_each_type = population_size//num_queries * 3

    # ------------- Remove Past Images ------------------------------------------------------------ #
    if os.path.exists(path):
        print("Removeing Past Downloads...")
        shutil.rmtree(path + '/', ignore_errors=False, onerror=None)
    if os.path.exists(dirName):
        print("Removeing Past Population...")
        shutil.rmtree(dirName + '/', ignore_errors=False, onerror=None)

    # ------------- Get Images From Internet-------------------------------------------------------------------- #
    print("Downloading " + str(images_of_each_type) + " images for each query...")
    response = google_images_download.googleimagesdownload()   #class instantiation

    arguments = {"keywords":query,"limit":images_of_each_type,"print_urls":verbose, "format":"jpg", "usage_rights":"labeled-for-nocommercial-reuse", "no_directory":True}   #creating list of arguments
    paths = response.download(arguments)   #passing the arguments to the function
    print(paths)   #printing absolute paths of the downloaded images

    # ------------- Make Folder for Population ----------------------------------------------------#
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory " , dirName ,  " Created ")
    else:    
        print("Directory " , dirName ,  " already exists")

    # -------------- Tidy Up Images ----------------------------------------------------------------#

    raw = []
    for filename in os.listdir(path + '/'):
        print("Cleaning up " + filename)
        try:
            src_image = Image.open(path + '/' + filename)
            raw.append(src_image)
            if src_image and population_count < population_size:
                new_image = src_image.resize((1024,1024), resample=0)
                population.append(new_image)
                #new_image.save(dirName + '/' + str(population_count) + '.png')
                population_count += 1
                del raw[-1]
        except:
            print("Cleanup Failed!")
            pass

    if population_count is population_size:
        print("\nSuccessfully Generated Initial Population")
    elif population_count > 0:
        print("\nFailed To Generate Some Members Of Initial Population")
        return None
    else:
        print("\nFailed To Generate Initial Population")
        return None
    print("Population Size: " + str(population_count))

    shuffle(population)

    # -------------- Create First Children -------------------------------------------------------- #
    new_population = []
    i = 0
    tried_combos = []
    while i < population_size:
        img_one = population[randint(0, population_size-1)]
        img_two = population[randint(0, population_size-1)]
        img_three = population[randint(0, population_size-1)]
        if img_one is not img_two and img_two is not img_three and img_one is not img_three:
            try:
                temp_image = Image.blend(img_one, img_two, 1/2)
                new_image = Image.blend(img_three, temp_image, 2/3)
                new_image.save('population/gen_1_individual_' + str(i) + '.png')
                new_population.append((new_image, 1))
                print(str(i+1) + " Images Merged")
                i += 1
            except:
                print("Images Failed To Blend!")

    population = new_population
    population_size = len(population)
    print("\nGenerated "+ str(population_size) +" Children")

    shuffle(new_population)

    return (new_population, raw)
