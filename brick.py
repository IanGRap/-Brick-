import genetic_algorithm
from download import generate_initial_population
from GUI_test import gui_creation_by_pixels
from PIL import Image
import sys
from random import randint, random, shuffle

def generate_next_generation(population, population_size, generation):
    i = len(population)
    initial_size = len(population)
    tried_combos = []
    while i < population_size:
        #get (image, fitness) pairs
        one = population[randint(0, len(population)-1)]
        two = population[randint(0, len(population)-1)]
        three = population[randint(0, len(population)-1)]

        #get image from pairs
        img_one = one[0]
        img_two = two[0]
        img_three = three[0]

        if img_one is not img_two and img_two is not img_three and img_one is not img_three:
            try:
                temp_image = Image.blend(img_one, img_two, 1/2)
                new_image = Image.blend(img_three, temp_image, 1/2)
                new_image.save('population/gen_' + str(generation) + '_individual_' + str(i) + '.png')
                
                #fitness of new image is average fitness of its parents
                new_image_fitness = (one[1] + two[1] + three[1])/3
                 
                population.append((new_image, new_image_fitness))
                print(str(i+1 - initial_size) + " Images Merged")
                i += 1
            except:
                print("Images Failed To Blend!")

    print("\nGenerated "+ str(population_size - initial_size) +" children in generation "+ str(generation))

    shuffle(population)

if __name__ == "__main__":
    # Proccess user query
    query = ""
    num_queries = 0
    for i in range(1, len(sys.argv)-1):
        query += sys.argv[i] + " texture,"
        num_queries += 1
    query += sys.argv[len(sys.argv)-1] + " texture"
    num_queries += 1
    population_size = 10
    verbose = True

    #raw_images = []
    # assign 60 raw images from google
    # raw_images = function(60)
    
    # initial array of doubles, image with fitness
    # all images start with fitness 1
    population = generate_initial_population(query, num_queries, population_size, verbose)
    generation = 1
    while True:
        
        # make sure we always have 20 images
        while len(population) < population_size:
            generation += 1
            #randomly blend 3 raw images together and add it to images
            generate_next_generation(population, population_size, generation)

        exited_peacefully = gui_creation_by_pixels(population)
        if not exited_peacefully:
            print("exited with X")
            exit(0)

        population.sort(key=lambda im: im[1], reverse=True)

        #remove images with a fitness of 0 or under
        population = [individual for individual in population if individual[1] > 0]