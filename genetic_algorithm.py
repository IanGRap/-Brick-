from PIL import Image
from random import random, choice

def crossover(image_one, image_two, fitness_one, fitness_two):
	"""
		Input: 2 images with fitness values to crossover
		Output: A single image made from linearly interpolating the input images
		Assuming image inputs are pillow images with the same size
	"""
	alpha = 0.5 + 0.49 * ((fitness_one - fitness_two)/(fitness_one + fitness_two))
	return Image.blend(image_one, image_two, alpha)

def mutate(im):
	v = int(random() * 30)
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
		

