# Importation of libraries
from tkinter import *
import customtkinter as ctk
from customtkinter import *
from CTkListbox import *
from PIL import Image, ImageTk
import pygame 
import os
from threading import *

ctk.set_appearance_mode("System") 
ctk.set_default_color_theme("blue")

# initialization of pygame
pygame.mixer.init()

#Store current position of the music
current_pos = 0
paused = False
selected_folder_path = ""

# functions 
class SlidePanel(CTkFrame):
	def __init__(self, parent, start_pos, end_pos):
		super().__init__(master = parent)
		# general attributes 
		self.start_pos = start_pos + 0.7
		self.end_pos = end_pos - 0.3
		self.width = abs(start_pos - end_pos)
		# animation logic
		self.pos = self.start_pos
		self.in_start_pos = True
		# layout
		self.place(relx = self.start_pos, rely = 0.05, relwidth = self.width, relheight = 0.9)
	def animate(self):
		if self.in_start_pos:
			self.animate_forward()
		else:
			self.animate_backwards()
	def animate_forward(self):
		if self.pos > self.end_pos:
			self.pos -= 0.008
			self.place(relx = self.pos, rely = 0.05, relwidth = self.width, relheight = 0.9)
			self.after(10, self.animate_forward)
		else:
			self.in_start_pos = False
	def animate_backwards(self):
		if self.pos < self.start_pos:
			self.pos += 0.008
			self.place(relx = self.pos, rely = 0.05, relwidth = self.width, relheight = 0.9)
			self.after(10, self.animate_backwards)
		else:
			self.in_start_pos = True
def smusicfolder():
    global selected_folder_path, song
    selected_folder_path = filedialog.askdirectory()
    if selected_folder_path:
        lbox.delete(0, END) # delete the first foler if a new one is selected 
        for song in os.listdir(selected_folder_path):
            if song.endswith(".mp3"):
                lbox.insert(END, song)
def previousmusic():
        current_index = lbox.curselection()
        if current_index > 0:
            lbox.deselect(current_index)
            lbox.activate(current_index - 1)
            play_selected_song()        
def nextmusic():
    current_index = lbox.curselection()
    if current_index < lbox.size() - 1:
        lbox.deselect(current_index)
        lbox.activate(current_index + 1)
        play_selected_song()   
def playmusic():
    global paused
    if paused: 
        pygame.mixer.music.unpause()
        paused= False
    else:
        play_selected_song()
def play_selected_song():
    global paused, full_path
    current_index = lbox.curselection()
    selected_song = lbox.get(current_index)
    full_path = os.path.join(selected_folder_path, selected_song)
    pygame.mixer.music.load(full_path)
    pygame.mixer.music.play(start=current_pos)
    paused=False
def pausemusic():
    global paused
    pygame.mixer.music.pause()
    paused = True
def stop_music():
    global paused
    pygame.mixer.music.stop() # stop played music and reset progress bar
    paused = False
def volume(value):
    pygame.mixer.music.set_volume(value)
def light():
    ctk.set_appearance_mode("light")
def dark():
    ctk.set_appearance_mode("dark")
    
# Window configuration
app = ctk.CTk()
app.minsize(700, 600)
app.geometry("800x700+400+60")
app.title("Music Player")
app.iconbitmap(r"C:\Users\gmwat\MusicPlayer\musiclogo.ico")

# creation of a frame
frame = CTkFrame(app, fg_color=('SlateGray4','grey24'))
frame.pack(side='bottom', padx=50, pady=10, anchor='s')

# creation of other buttons
playbt = CTkButton(frame, text='|>', width=5, fg_color=('RoyalBlue1','blue'),
                   hover_color=('RoyalBlue3','blue2'), command=playmusic)
playbt.pack(padx=15, pady=10, side='left', expand=True)
pausebt = CTkButton(frame, text='| |', width=5, fg_color=('RoyalBlue1','blue'),
                    hover_color=('RoyalBlue3','blue2'),command=pausemusic)
pausebt.pack(padx=15, pady=10, side='left', expand=True)
nextbt = CTkButton(frame, text='>', width=5, fg_color=('RoyalBlue1','blue'),
                   hover_color=('RoyalBlue3','blue2'), command=nextmusic)
nextbt.pack(padx=15, pady=10, side='left', expand=True)
previousbt = CTkButton(frame, text='<', width=5, fg_color=('RoyalBlue1','blue'),
                       hover_color=('RoyalBlue3','blue2'), command=previousmusic)
previousbt.pack(padx=15, pady=10, side='left', expand=True)
select_music_folder = CTkButton(app,text='Select Music Folder', text_color=('white','RoyalBlue1'), width=100,
                     fg_color=('SlateGray4','grey24'), hover_color=('RoyalBlue3','grey28'), command=smusicfolder)
select_music_folder.place(x=20, y=50)

# progress bar
pbar = CTkProgressBar(app, width=200)
pbar.pack(padx=10, pady=10, side='bottom')

slider = CTkSlider(app, from_=0, to=1, width=130, height= 15, command=volume)
slider.pack(side='bottom',pady=10)

# create a new frame
frame2 = CTkFrame(app, fg_color=('transparent'))
frame2.pack(side='left', padx=10, pady=50, anchor='s', fill='x', expand=True)

# upload images 
backg = Image.open(r'gmwat\MusicPlayer\background7.png')
backg = backg.resize((405, 355))
backg = ImageTk.PhotoImage(backg)
app_img = Label(frame2, width=400, height=350, image=backg, padx=10)
app_img.pack(padx=30, pady=10, side='left')
    
# create listbox
lbox = CTkListbox(frame2, width=300, height=270,fg_color=('dodger blue', 'black'))
lbox.pack(padx=30, pady=10, side='right')

# creation of animated widget
animated_panel = SlidePanel(app, 1.0, 0.7)

# creation of buttons
button = CTkButton(app, text = 'Menu', command = animated_panel.animate, width=100, height=25,
                   text_color=('white','RoyalBlue1'), fg_color=('SlateGray4','grey24'), hover_color=('RoyalBlue3','grey28'))
button.place( x=20, y=20)

# creation of light and dark mode 
LightMode = CTkButton(animated_panel, text='Light Mode', text_color=('white','RoyalBlue1'), width=100,
                     fg_color=('SlateGray4','grey24'), hover_color=('RoyalBlue3','grey28'), command=light)
LightMode.pack(fill='x')
DarkMode = CTkButton(animated_panel, text='Dark Mode', text_color=('white','RoyalBlue1'), width=100,
                     fg_color=('SlateGray4','grey24'), hover_color=('RoyalBlue3','grey28'), command=dark)
DarkMode.pack(fill='x')

# Creation of help label 
help_label = CTkLabel(animated_panel, justify='left', padx=1, pady=10, anchor='n', 
                      text='Welcome to the best \nMusic Player of the world\n\n'
                      'How to use the commands :\n|> : Play music\n|| : Pause music'
                      '\n< : Previous music\n> : Next music')
help_label.pack(fill='both', expand=True)

app.mainloop()
