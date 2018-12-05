from tkinter import *
from os import listdir
import os.path
from PIL import Image, ImageTk
from functools import partial

#method for each button
def test_method(image_path): 
	print(image_path)

#get population from whatever folder
pop_loc = "C:/Users/Paula NU/Pictures/picturess/" 
population = listdir(pop_loc)

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
for individual in population:

	#image button "wrapping" 
	if col_index > 10:
		col_index = 0
		row_index = row_index + 1	

	filepath = pop_loc + individual
	image = Image.open(filepath)
	image = image.resize((230,230), resample = 0) #images are 1024x1024 originally
	individual = ImageTk.PhotoImage(image)

	#store image to prevent the trash collection from deleting it
	image_list.append(individual)

	#create buttons
	action_with_arg = partial(test_method, filepath) #dynamically create button actions
	button_list.append(Button(button_grid, command = action_with_arg))
	button_list[list_index].config(image = individual)
	button_list[list_index].grid(row = row_index, column = col_index, padx = 5, pady = 5)

	col_index = col_index + 1
	list_index = list_index + 1

T = Label(text_frame, text="Select ur fav!")
T.config(font=("Courier", 36))
T.pack(side=TOP, padx=5, pady=5)
	
root.mainloop()

