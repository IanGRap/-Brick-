from PIL import Image, ImageFilter
from random import random, choice, shuffle

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
    return (mutate(Image.blend(image_one, image_two, alpha)), (fitness_one + fitness_two)/2)

def mutate(im):
    if(random() > 0.2):
        return im
    width, height = im.size
    v = int(random() * 50) + 10
    vr = int(((random() * 2) - 1) * v)
    vg = int(((random() * 2) - 1) * v)
    vb = int(((random() * 2) - 1) * v)
    colors = {}
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
    r = choice(range(3))
    magnitude = int((0.5 * width) * random()) + int(0.25 * width)
    if(r is 0):
        area_one = (0, 0, magnitude, height)
        area_two = (magnitude + 1, 0, width, height)
        crop_one = im.crop(area_one)
        crop_two = im.crop(area_two)
        w = crop_two.size[0]
        im.paste(crop_two)
        im.paste(crop_one, (w, 0))
    elif(r is 1):
        area_one = (0, 0, width, magnitude)
        area_two = (0, magnitude + 1, width, height)
        crop_one = im.crop(area_one)
        crop_two = im.crop(area_two)
        h = crop_two.size[1]
        im.paste(crop_two)
        im.paste(crop_one, (0, h))
    else:
        mid = (int(random() * width), int(random() * height))
        crop_tl = im.crop((0, 0, mid[0], mid[1]))
        crop_bl = im.crop((0, mid[1] + 1, mid[0], height))
        crop_tr = im.crop((mid[0] + 1, 0, width, mid[1]))
        crop_br = im.crop((mid[0] + 1, mid[1] + 1, width, height))
        im.paste(crop_br)
        im.paste(crop_bl, (crop_br.size[0], 0))
        im.paste(crop_tr, (0, crop_br.size[1]))
        im.paste(crop_tl, (crop_br.size[0], crop_br.size[1]))
    return im.filter(ImageFilter.SHARPEN)
        
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
