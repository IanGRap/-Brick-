from PIL import Image
from random import random

good_fitness = 3

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
    parents = List()

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

    results = shuffle(parents)
    nextGen = List()

    for i in range(1, len(parents)):
        if len(nextGen) < len(images):
            nextGen.append(crossover(parents[i-1], parents[i]))

    nextGen.append(crossover(parents[0], parents[len(parents)-1]))
