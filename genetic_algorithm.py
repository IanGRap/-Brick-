from PIL import Image
from random import random

good_fitness = 3

def crossover(image_one, image_two, fitness_one, fitness_two):
	"""
		Input: 2 images with fitness values to crossover
		Output: A single image made from linearly interpolating the input images
		Assuming image inputs are pillow images with the same size
	"""
	alpha = 0.5 + 0.49 * ((fitness_one - fitness_two)/(fitness_one + fitness_two))
	return Image.blend(image_one, image_two, alpha)

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
