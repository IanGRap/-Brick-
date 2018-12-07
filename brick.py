import genetic_algorithm
from download import generate_initial_population
from GUI_test import gui_creation
from PIL import Image
import sys

if __name__ == "__main__":
    # Proccess user query
    query = ""
    num_queries = 0
    for i in range(1, len(sys.argv)-1):
        query += sys.argv[i] + " texture,"
        num_queries += 1
    query += sys.argv[len(sys.argv)-1] + " texture"
    num_queries += 1
    population_size = 20
    verbose = True

    #raw_images = []
    # assign 60 raw images from google
    # raw_images = function(60)

    images = generate_initial_population(query, num_queries, population_size, verbose)
    # initial array of doubles, image with fitness
    # all images start with fitness 1

    gui_creation(images)

    """
    # loop until user ends program
    while True:

        # make sure we always have 20 images
        while len(images) < 20:
            pass
            #randomly blend 3 raw images together and add it too images

        # mutate images
        for im in images:
            genetic_algorithm.mutate(im[0], im[1])

        # sort images by highest fitness
        images.sort(key=lambda im: im[1], reverse=True)

        # input first 10 images into gui function
        # images = function(images[:10])
        pass
    """