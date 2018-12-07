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

#method for each button
def test_method(image): 
	print(image)


def gui_creation(population_list):

	root = Tk()

	#frame for image buttons
	button_grid =Frame(root)
	button_grid.pack(side=TOP,fill=X)

	#frame for the text
	text_frame=Frame(root)
	text_frame.pack(side=TOP, fill=X)

	#initialize
	col_index = 0
	list_index = 0
	row_index = 0

	#create buttons from population
	button_list = []
	image_list = []
	individuals = [i[0] for i in population_list[:10]]
	for individual in individuals:

		#image button "wrapping" 
		if col_index > 4:
			col_index = 0
			row_index = row_index + 1	

		individual = individual.resize((230,230), resample = 0) #images are 1024x1024 originally
		individual = ImageTk.PhotoImage(individual)

		#store image to prevent the trash collection from deleting it
		image_list.append(individual)

		#create buttons
		action_with_arg = partial(test_method, individual) #dynamically create button actions
		button_list.append(Button(button_grid, command = action_with_arg))
		button_list[list_index].config(image = individual)
		button_list[list_index].grid(row = row_index, column = col_index, padx = 5, pady = 5)

		col_index = col_index + 1
		list_index = list_index + 1

		print("ayyy")

	T = Label(text_frame, text="Select ur fav!")
	T.config(font=("Courier", 36))
	T.pack(side=TOP, padx=5, pady=5)
		
	root.mainloop()


#test that shit out bc i dont feel like using python command line
if __name__ == '__main__':
	pop_loc = "C:/Users/Paula NU/Pictures/picturess/" 
	population = listdir(pop_loc)

	fit_population = []

	for individual in population:
		filepath = pop_loc + individual
		image = Image.open(filepath)
		fit_population.append((image, 1))

	gui_creation(fit_population)



