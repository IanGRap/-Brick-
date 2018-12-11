from PIL import Image
from random import random, shuffle

good_fitness = 3

def crossover(individual_one, individual_two):
    """
        Input: 2 images with fitness values to crossover
        Output: A single image made from linearly interpolating the input images
        Assuming image inputs are pillow images with the same size
    """
    image_one = individual_one[0]
    image_two = individual_one[0]
    fitness_one = individual_one[1]
    fitness_two = individual_two[1]
    alpha = 0.5 + 0.49 * ((fitness_one - fitness_two)/(fitness_one + fitness_two))
    return (Image.blend(image_one, image_two, alpha), (fitness_one + fitness_two)/2)

def mutate(im, fitness):
    v = (good_fitness/fitness) * 30
    vr = int(random() * v)
    vg = int(random() * v)
    vb = int(random() * v)
    colors = {}
    width, height = im.size
    for x in range(width):
        for y in range(height):
            r,g,b = im.getpixel((x,y))
            if (r, g, b) in colors:
                im.putpixel((x, y), colors[(r, g, b)])
            else:
                nr = min(max(0, r + vr), 255)
                ng = min(max(0, g + vg), 255)
                nb = min(max(0, b + vb), 255)
                colors[(r, g, b)] = (nr, ng, nb)
                im.putpixel((x, y), (nr, ng, nb))

def adjust_color_value(c):
    if random() < 0.5:
        return int(c + (255 - c) * random())
    else:
        return int(c - c * random())

def generate_successors(images):
    """
        Input: List of (image, fitness) after user has evaluated
        Output: List of next gen
    """
    parents = []

    Sum = 0
    for im, fit in images:
        Sum += fit

    images.sort(key=lambda im: im[1], reverse=True)
    while len(parents) < len(images) // 2:
        p_low = 0
        p_high = 0
        rand = random()

        for tup in images:
            # tup is a tuple: (img, fitness)
            p_low = p_high
            p_high += tup[1] / Sum
            if p_low <= rand and rand < p_high and tup not in parents:
                parents.append(tup)

    nextGen = []

    while len(nextGen) < len(images):
        shuffle(parents)
        for i in range(1, len(parents)):
            if len(nextGen) < len(images):
                nextGen.append(crossover(parents[i-1], parents[i]))

    return nextGen
