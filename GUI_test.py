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
image_list = []
button_list = []
submitted = []

# method for each button
def show_image(image): 
    image.show()

def on_upvote(individual, index):
    if upvote_button_list[index].cget("relief") == RAISED:
        upvote_button_list[index].config(relief=SUNKEN, bg = "#ffffff")
        if downvote_button_list[index].cget("relief") == SUNKEN:
            downvote_button_list[index].config(relief = RAISED, bg = "#cccccc")
    else:
        upvote_button_list[index].config(relief=RAISED, bg = "#cccccc")

def on_downvote(individual, index):
    if downvote_button_list[index].cget("relief") == RAISED:
        downvote_button_list[index].config(relief=SUNKEN, bg = "#ffffff")
        if upvote_button_list[index].cget("relief") == SUNKEN:
            upvote_button_list[index].config(relief = RAISED, bg = "#cccccc")
    else:
        downvote_button_list[index].config(relief=RAISED, bg = "#cccccc")

def save_image(image):
	fileNum = 1
	while True: 
		output = "output" + str(fileNum) + ".png"
		exists = os.path.isfile(output)
		if not exists:
			image.save(output)
			print("output to ", output)
			break
		fileNum += 1

def submit_ratings(population, root):
    for i in range(10):
        if upvote_button_list[i].cget("relief") == SUNKEN:
            population[i] = (population[i][0], population[i][1] + 1)
        if downvote_button_list[i].cget("relief") == SUNKEN:
            population[i] = (population[i][0], population[i][1] - 1)

    # clear lists in preperation for next function call
    upvote_button_list.clear()
    downvote_button_list.clear()
    image_list.clear()
    button_list.clear()

    # mark exit type as submitted
    submitted.append(True)

    root.destroy()

def gui_creation_by_pixels(population):
    
    root = Tk()
    root.geometry("1310x720")
    root.configure(background='#cccccc')

    # get up and down button images
    up_image = Image.open("up.png")
    down_image = Image.open("down.png")
    display_up = ImageTk.PhotoImage(up_image)
    display_down = ImageTk.PhotoImage(down_image)

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
            image_button.place(x=j*261 + 5, y=i*298 + 5, in_=root)

            # create up button
            up_action = partial(on_upvote, population[image_index], image_index) #dynamically create button actions
            up_button = Button(root, command = up_action, image = display_up, borderwidth=0, bg = "#cccccc")
            upvote_button_list.append(up_button)
            up_button.place(x=j*261 + 5,y=i*298 + 261 + 5, in_=root)

            # create down button    
            down_action = partial(on_downvote, population[image_index], image_index) #dynamically create button actions
            down_button = Button(root, command = down_action, image = display_down, borderwidth=0, bg = "#cccccc")
            downvote_button_list.append(down_button)
            down_button.place(x=j*261 + 37 + 5,y=i*298 + 261 + 5, in_=root)

            # create save button
            save_action = partial(save_image, population[image_index][0])
            save_button = Button(root, command = save_action, text = "Save", font = ("Courier", 12))
            button_list.append(save_button)
            save_button.place(x=j*261 + 74 + 5, y=i*298 + 261 + 5, in_=root)

            image_index += 1

    # create save button
    submit_action = partial(submit_ratings, population, root)
    submit_button = Button(root, command = submit_action, text = "Submit", font = ("Courier", 20))
    button_list.append(submit_button)
    submit_button.place(x=800, y=606, in_=root)

    prompt = Label(root, font = ("Courier", 18), width=40, height= 2, text="Vote on these images and then press\nsubmit for the next generation", bg="#cccccc")
    prompt.place(x=100,y=606,in_=root)

    root.mainloop()

    successful_exit = False

    if len(submitted) > 0:
        successful_exit = True
        submitted.clear()

    return successful_exit
