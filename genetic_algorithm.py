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

# def mutate(im, mutate_percent):
# 	width, height = im.size
# 	for x in range(width):
# 	    for y in range(height):
# 	    	if random() < mutate_percent:
# 		        r,g,b = im.getpixel((x,y))
# 		        r = adjust_color_value(r)
# 		        g = adjust_color_value(g)
# 		        b = adjust_color_value(b)
# 		        im.putpixel((x, y), (r, g, b))

def mutate(im):
	vr = round(random() * 2) - 1
	vg = round(random() * 2) - 1
	vb = round(random() * 2) - 1
	colors = {}
	width, height = im.size
	for x in range(width):
	    for y in range(height):
	        r,g,b = im.getpixel((x,y))
	        if (r, g, b) in colors:
	        	im.putpixel((x, y), colors[(r, g, b)])
	        else:
	        	v = round(random() * 100)
	        	nr = min(max(0, r + v * vr), 255)
	        	ng = min(max(0, g + v * vg), 255)
	        	nb = min(max(0, b + v * vb), 255)
	        	colors[(r, g, b)] = (nr, ng, nb)
	        	im.putpixel((x, y), (nr, ng, nb))

def adjust_color_value(c):
	if random() < 0.5:
		return int(c + (255 - c) * random())
	else:
		return int(c - c * random())
