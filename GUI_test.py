from tkinter import *
from os import listdir
import os.path
from PIL import Image, ImageTk

#method for each button
def test_method(): 
	print("lmao")

#get population from whatever folder
pop_loc = "C:/Users/Paula NU/Pictures/picturess/" 
population = listdir(pop_loc)

root = Tk()

#1 frame for image buttons
button_grid =Frame(root)
button_grid.pack(side=TOP,fill=X)

#1 frame for the text
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
	

	image = Image.open(pop_loc + individual)
	individual = ImageTk.PhotoImage(image)
	image_list.append(individual)

	#create bootons
	button_list.append(Button(button_grid, command = test_method))
	button_list[list_index].config(image = individual, width="40",height="40")
	button_list[list_index].grid(row = row_index, column = col_index, padx = 5, pady = 5)

	col_index = col_index + 1
	list_index = list_index + 1

T = Text(text_frame, height=1, width=50)
T.insert(END, "Select yo fav")
T.configure(state = 'disabled')
T.pack(side=TOP, padx=5, pady=5)



print(button_list)
	
#adding widgets
root.mainloop()

