import os
from google_images_download import google_images_download   #importing the retrival library
from PIL import Image
from random import randint

# ------------- Proccess User input ----------------------------------------------------------- #
query = "brick texture .png"
population_size = 20
verbose = True

# ------------- Get Images -------------------------------------------------------------------- #
response = google_images_download.googleimagesdownload()   #class instantiation

arguments = {"keywords":query,"limit":population_size,"print_urls":verbose}   #creating list of arguments
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
path = 'downloads/'+ query +'/'
count = 0

for filename in os.listdir(path):
    print(filename)
    img_file = open(path + filename, 'r')

