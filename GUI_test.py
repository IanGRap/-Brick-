from tkinter import *
from os import listdir
import os.path
from PIL import Image, ImageTk
from functools import partial

"""
-----------------------GUI FOR EACH GENERATION-------------------------
This will change the fitness values for each 
Takes in a list of tuples with (individual Image, fitness)
	values:
		< 0 --> garbage, throw that shit out
		= 1 --> neutral
		> 1 --> v good

The GUI will display the top individuals with the top 10 highest fitness values.
The user can upvote and downvote each image, or not do anything. 

Upvotes will add 1 to the fitness for that crossovered image. Downvotes will subtract 1. 

Don't worry too much about the math lmfao

"""

# "class" variables
upvote_button_list = []
downvote_button_list = []

# method for each button
def show_image(image): 
	image.show()

def on_upvote(individual, index):
	if upvote_button_list[index].cget("relief") == RAISED:
		upvote_button_list[index].config(relief=SUNKEN, bg = "#000000")
		if downvote_button_list[index].cget("relief") == SUNKEN:
			downvote_button_list[index].config(relief = RAISED, bg = "#ffffff")
	else:
		upvote_button_list[index].config(relief=RAISED, bg = "#ffffff")

def on_downvote(individual, index):
	if downvote_button_list[index].cget("relief") == RAISED:
		downvote_button_list[index].config(relief=SUNKEN, bg = "#000000")
		if upvote_button_list[index].cget("relief") == SUNKEN:
			upvote_button_list[index].config(relief = RAISED, bg = "#ffffff")
	else:
		downvote_button_list[index].config(relief=RAISED, bg = "#ffffff")

def save_image(image):
	image.save("output.png")

def gui_creation_by_pixels(population):

	root = Tk()
	root.geometry("1300x852")
	root.configure(background='#cccccc')

	# get up and down button images
	up_image = Image.open("up.png")
	down_image = Image.open("down.png")
	display_up = ImageTk.PhotoImage(up_image)
	display_down = ImageTk.PhotoImage(down_image)

	image_list = []
	button_list = []

	# create buttons from population
	image_index = 0
	for i in range(2):
		for j in range(5):
			display_individual = population[image_index][0].copy().resize((256,256), resample = 0) #images are 1024x1024 originally
			display_individual = ImageTk.PhotoImage(display_individual)

			# store image to prevent the trash collection from deleting it
			image_list.append(display_individual)

			# create image button
			show = partial(show_image, population[image_index][0]) #dynamically create button actions
			image_button = Button(root, command = show, image = display_individual, borderwidth=0)
			button_list.append(image_button)
			image_button.place(x=j*261, y=i*298, in_=root)

			# create up button
			up_action = partial(on_upvote, population[image_index], image_index) #dynamically create button actions
			up_button = Button(root, command = up_action, image = display_up, borderwidth=0)
			upvote_button_list.append(up_button)
			up_button.place(x=j*261,y=i*298 + 261, in_=root)

			# create down button		
			down_action = partial(on_downvote, population[image_index], image_index) #dynamically create button actions
			down_button = Button(root, command = down_action, image = display_down, borderwidth=0)
			downvote_button_list.append(down_button)
			down_button.place(x=j*261+37,y=i*298 + 261, in_=root)

			# create save button
			save_action = partial(save_image, population[image_index][0])
			save_button = Button(root, command = save_action, text = "Save", font = ("Courier", 12))
			button_list.append(save_button)
			save_button.place(x=j*261+74, y=i*298 + 261, in_=root)

			image_index += 1

	root.mainloop()

# test that shit out bc i dont feel like using python command line
if __name__ == '__main__':
	pop_loc = "C:/Users/Paula NU/Pictures/picturess/" 
	population = listdir(pop_loc)

	fit_population = []

	for individual in population:
		filepath = pop_loc + individual
		image = Image.open(filepath)
		fit_population.append((image, 1))

	gui_creation(fit_population)



