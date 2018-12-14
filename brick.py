from genetic_algorithm import *
from download import generate_initial_population
from GUI_test import gui_creation_by_pixels
from PIL import Image, ImageChops
import sys
from random import randint, random, shuffle, randrange
import argparse

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

def restock(population, population_size, raw):
    print("restocking...")
    if len(raw) > 0:
        while len(population) < population_size:
            if len(raw) is 0:
                return False
            image_to_clean = raw.pop(randrange(len(raw)))
            print("Cleaning up " + str(image_to_clean))
            try:
                if image_to_clean and len(population) < population_size:
                    new_image = image_to_clean.resize((1024,1024), resample=0)
                    population.append((Image.blend(new_image, population[randrange(len(population))][0], 0.5), 1))
            except:
                print("Cleanup Failed!")
                pass
        return True
    return False

def remove_duplicates(population):
    identical_count = 0
    different_count = 0
    individuals_to_remove = []
    for i in range(len(population)):
            for j in range(i+1, len(population)):
                if i is not j:
                    individual_one = population[i]
                    individual_two = population[j]
                    diff = ImageChops.difference(individual_one[0], individual_two[0])
                    if not diff.getbbox():
                        if individual_one[1] < individual_two[1]:
                            individuals_to_remove.append(j)
                        else:
                            individuals_to_remove.append(i)
                        identical_count += 1 
                    else:
                        different_count += 1
    print("Removing " +  str(len(individuals_to_remove)) + " from a population of " + str(len(population)))
    for i in individuals_to_remove:
        print("Removing the " + str(i) + " image")
        population[i] = None
    del individuals_to_remove
    print("There are " + str(identical_count) + " pairs of identical images")
    print("There are " + str(different_count) + " pairs of different images")
    return [x for x in population if x is not None]

if __name__ == "__main__":
    # Proccess user query
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--freeuse", help="If used images will be in the public domain", action="store_true")
    parser.add_argument("-s", "--safesearch", help="If used safesearch is enabled", action="store_true")
    parser.add_argument("-t", "--texture", help="If used textures are searched for", action="store_true")
    parser.add_argument("-k", "--keyword",help="The keyword or keywords used to generate the initial population")
    parser.add_argument("-c", "--count",help="The count of images to be pulled from the web as reference",type=int)
    args = parser.parse_args()

    queries = args.keyword.split()
    query = ""
    num_queries = 1
    if len(queries) == 0:
        print("Required flag -k or --keyword to generate initial population")
        exit(0)
    for i in range(len(queries)-1):
        query += queries[i]
        if args.texture:
            query += " texture"
        query += ","
        num_queries += 1
    query += queries[-1]
    if args.texture:
            query += " texture"
    verbose = True
    population_size = 10
    copyright = "labeled-for-nocommercial-reuse"
    if args.freeuse:
        copyright = "labeled-for-reuse"
    if args.count:
        download_count = args.count
    else:
        download_count = 40

    # initial array of doubles, image with fitness
    # all images start with fitness 1
    population, raw = generate_initial_population(query, num_queries, population_size, download_count, verbose, copyright, args.safesearch)
    generation = 1
    
    while True:

        print("\n ~--- Starting Generation ", generation, " ---~\n")

        # Force RGB incoding
        for individual in population:
            if individual[0].mode != "RGB":
                print("Image Converted")
                individual[0].convert(mode="RGB")

        #remove images with a fitness of 0 or under
        population = [individual for individual in population if individual[1] > 0]

        population = remove_duplicates(population)
        
        # make sure we always have 20 images
        if len(population) < population_size:
            if not restock(population, population_size, raw):
                #randomly blend 3 raw images together and add it to images
                generate_next_generation(population, population_size, generation)

        shuffle(population)

        population.sort(key=lambda im: im[1], reverse=True)

        exited_peacefully = gui_creation_by_pixels(population)
        if not exited_peacefully:
            print("exited with X")
            exit(0)

        #remove images with a fitness of 0 or under
        population = [individual for individual in population if individual[1] > 0]

        population = remove_duplicates(population)
        
        # make sure we always have 20 images
        if len(population) < population_size:
            if not restock(population, population_size, raw):
                #randomly blend 3 raw images together and add it to images
                generate_next_generation(population, population_size, generation)

        generation += 1

        population = generate_successors(population)

        population.sort(key=lambda im: im[1], reverse=True)

        print("Population After Crossover")
        i = 0
        for individual in population:
            print("The number " + str(i) + " Image has fitness " + str(individual[1]))
            i += 1
