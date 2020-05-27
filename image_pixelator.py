"""
File: image_pixelator.py
---------------------------
This program is a tool that pixelates an image.
"""

"""
HOW TO USE PROGRAM:

1. Save an image into the imagebank folder

2. Type filename (ex. 'imagebank/nightart.jpg' ) into the IMAGE constant

3. Run program in terminal
     a. Window displaying the image, a scale and a button should appear 
     
4. Use scale to select pixelation level

5. Click pixelate  

6. Pixelated image will appear in another window
"""


from tkinter import *
from PIL import ImageTk,Image
from simpleimage import SimpleImage



#Put the image filename here
#AS THE PROGRAM STANDS, THE IMAGE WIDTH AND HEIGHT MUST BE LESS THAN 1000px
IMAGE = ''


#This variable determines the size of the GUI window.
#Increase this number to contain images with a width and height larger than 1000px
CANVAS_SIZE = 650




######################### FUNCTIONS ###############################

root = Tk()
root.title('Image Pixelator')

"""
The following functions resize the image to fit on the graphical user interface.
"""

def resize_height():
    image = SimpleImage(IMAGE)
    height_value = image.height
    # reduces height size by factor of 3
    if height_value > 300:
        height_value //= 3
    return height_value


def resize_width():
    image = SimpleImage(IMAGE)
    width_value = image.width
    #reduces width size by factor of 3
    if width_value > 300:
        width_value //= 3
    return width_value




"""
The following functions pixelate the image and display it in a new window.
"""

#This the main function for pixeltion.
#It creates a pixelated image using the pixel factor assigned by the slider scale
#and displays that image  in a new window.
def make_pixelated_image(pixel_factor):
    #Pulls image width and height information from image
    image = SimpleImage(IMAGE)
    image_width = image.width
    image_height = image.height
    pixelated_image = pixelate_image(image, image_height, image_width, pixel_factor)
    #displays pixelated image in new window
    pixelated_image.show()


# pixelates image by creating a new image that uses less pixel information
def pixelate_image(image, height, width, pixel_factor):
    #creates the new image canvas
    new_width, new_height = determine_canvas_size(width, height, pixel_factor)
    result_image = SimpleImage.blank(new_width, new_height)
    #for-each loop selects which pixels will be kept for new image
    # and reprints them on the canvas
    for pixel in image:
        x = pixel.x
        y = pixel.y
        #uses pixel factor to determine which pixels are kept
        if (x % pixel_factor == 0) and (y % pixel_factor == 0):
            px = image.get_pixel(x, y)
            result_image.set_pixel(x, y, px)
            # reprints selected pixel in empty space in new image canvas
            result_image = fill_out_pixel(x, y, px, result_image, pixel_factor)
    return result_image

#reprints selected pixel in empty space on image
def fill_out_pixel(x, y, px, result_image, pixel_factor):
    #the size of each pixel in pixelated image is the same as pixel factor
    for n in range(pixel_factor):
        for i in range(pixel_factor):
            result_image.set_pixel(x + i, y, px)
        y += 1
    return result_image

#determines size of canvas for new pixelated image
#if pixel factor is greater than 2, size of new image will increase
def determine_canvas_size(image_width, image_height, pixel_factor):
    canvas_width = determine_width(image_width, pixel_factor)
    canvas_height = determine_height(image_height, pixel_factor)
    return canvas_width, canvas_height


def determine_width(image_width, pixel_factor):
    #identifies how many pixels will be sampled
    amt_samples = determine_amt_of_samples(image_width, pixel_factor)
    canvas_width = amt_samples * pixel_factor
    return canvas_width

def determine_height(image_height, pixel_factor):
    amt_samples = determine_amt_of_samples(image_height, pixel_factor)
    canvas_height = amt_samples * pixel_factor
    return canvas_height


#identifies how many pixels will be sampled according to the length of image's side
def determine_amt_of_samples(side_length, pixel_factor):
    amt_samples = (side_length - 1) // pixel_factor
    amt_samples += 1
    return amt_samples





######################## GRAPHICAL USER INTERFACE ################################

canvas = Canvas(root, height=CANVAS_SIZE, width=CANVAS_SIZE)
canvas.pack()




background = Label(canvas, bg='#ffb3d9')
background.place(relwidth=1, relheight=1)



#Black shadow below title
#label contains text to make it equal size as tile
main_title_frame = Label(background,
                         text='Image Pixelator',
                         font='Courier 50',
                         bg='black',
                         padx=10,
                         pady=10,
                         anchor=CENTER)
main_title_frame.place(relx=0.16, rely=0.05)



#Title Label
main_title = Label(background,
                   text='Image Pixelator',
                   font='Courier 50',
                   padx=10,
                   pady=10,
                   anchor=CENTER)
main_title.pack(pady=20)



"""
This displays the image within the GUI window
"""
#opens and resizes image using Image module
img = Image.open(IMAGE)
img = img.resize((resize_width(),resize_height()), Image.ANTIALIAS)
#displays image on interface using ImageTK module
image_to_edit = ImageTk.PhotoImage(img)
image_label = Label(background,
                    image=image_to_edit,
                    bg='white',
                    bd=10,
                    anchor=CENTER)
image_label.pack(pady=20)




#Directions label above slider
scale_text = Label(background,
                   text='Move scale to increase pixelation',
                   font='Courier 17',
                   bg='white',
                   fg='black')
scale_text.pack(anchor=CENTER)



#Pixelation slider scale
pixelation_scale = Scale(background,
                    orient=HORIZONTAL,
                    length=300,
                    sliderlength=10,
                    from_=1,
                    font='Courier 30',
                    fg='black',
                    troughcolor='black')
pixelation_scale.pack(anchor=CENTER, pady=15)



#Pixelate button
pixelate_button = Button(background,
                          text='PIXELATE',
                          fg='#000000',
                          relief=RAISED,
                          borderwidth=40,
                          font='Courier 30',
                          highlightbackground='white',
                          command= lambda: make_pixelated_image(pixelation_scale.get()))
pixelate_button.pack(anchor=CENTER, pady=30)




root.mainloop()

######################### REFERENCES & RESOURCES #############################

"""
This program is pixelation algorithm that simulates Nearest-Neighbor interpolation 
in image sampling.

More references and information can be found  below.


Article explaining Nearest-Neighbor Interpolation:
https://www.giassa.net/?page_id=207


Tkinter programming guide:
https://www.tutorialspoint.com/python/python_gui_programming.htm



"""