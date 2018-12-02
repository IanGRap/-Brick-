from PIL import Image
from random import random

def crossover(image_one, image_two, fitness_one, fitness_two):
	"""
		Input: 2 images with fitness values to crossover
		Output: A single image made from linearly interpolating the input images
		Assuming image inputs are pillow images with the same size
	"""
	alpha = 0.5 + 0.49 * ((fitness_one - fitness_two)/(fitness_one + fitness_two))
	return Image.blend(image_one, image_two, alpha)

def mutate(im, mutate_percent):
	width, height = im.size
	for x in range(width):
	    for y in range(height):
	    	if random() < mutate_percent:
		        r,g,b = im.getpixel((x,y))
		        r = adjust_color_value(r)
		        g = adjust_color_value(g)
		        b = adjust_color_value(b)
		        im.putpixel((x, y), (r, g, b))

def adjust_color_value(c):
	if random() < 0.5:
		return int(c + (255 - c) * random())
	else:
		return int(c - c * random())
