import genetic_algorithm
from PIL import Image
import sys

if __name__ == "__main__":
	raw_images = []
	# assign 60 raw images from google
	# raw_images = function(60)

	images = []
	# array of doubles, image with fitness
	# all images start with fitness 1

	# loop until user ends program
	while True:

		# make sure we always have 20 images
		while len(images) < 20:
			#randomly blend 3 raw images together and add it too images

		# mutate images
		for im in images:
			genetic_algorithm.mutate(im[0], im[1])

		# sort images by highest fitness
		images.sort(key=lambda im: im[1], reverse=True)

		# input first 10 images into gui function
		# images = function(images[:10])