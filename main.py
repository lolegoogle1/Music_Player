import tkinter
import pygame
from tkinter import filedialog

root = tkinter.Tk()
root.title('My MP3 Player')
root.geometry("500x300")

# Initialize Pygame Mixer
pygame.mixer.init()

global paused
paused = False


# Add Song Function
def add_song() -> None:
    def strip_song(raw_song: str) -> str:
        return raw_song.split("/")[-1].split('.')[0].replace("_", " ").replace("-", " - ")

    song = filedialog.askopenfilename(initialdir='/home/oleh/Downloads/audio_samples', title="Choose a Song",
                                      filetypes=(("mp3 Files", "*.mp3"),))
    song_name = strip_song(song)
    song_box.insert(tkinter.END, song)


# Add a few songs
def add_songs() -> None:
    songs = filedialog.askopenfilenames(initialdir='/home/oleh/Downloads/audio_samples', title="Choose songs",
                                        filetypes=(("mp3 Files", "*.mp3"),))

    # Loop through song list and replace directory info and mp3
    for song in songs:
        song_box.insert(tkinter.END, song)  # Insert into playlist


# Play selected song
def play(is_paused) -> None:
    global paused
    paused = is_paused

    if paused:
        # Unpause the song
        pygame.mixer.music.unpause()
        paused = False
        return

    song = song_box.get(tkinter.ACTIVE)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    if song_box.curselection() == ():
        # New song bar
        # song_box.activate(0)

        # Set Active Bar to the previous song
        song_box.selection_set(0, last=None)


# Stop selected song
def stop() -> None:
    pygame.mixer.music.stop()
    song_box.selection_clear(tkinter.ACTIVE)


# Play previous song
def previous_song() -> None:
    previous_number = song_box.curselection()[0] - 1
    if previous_number < 0:
        previous_number = song_box.size() - 1
        previous_one = song_box.get(previous_number)
    else:
        previous_one = song_box.get(previous_number)

    # Load and play song
    pygame.mixer.music.load(previous_one)
    pygame.mixer.music.play(loops=0)

    # Clear active bar in playlist listbox
    song_box.selection_clear(0, tkinter.END)

    # New song bar
    song_box.activate(previous_number)

    # Set Active Bar to the previous song
    song_box.selection_set(previous_number, last=None)


# Play the next song
def next_song() -> None:
    # Get the current song tuple number and add 1 to it
    # next_song_number = song_box.curselection()[0] + 1

    next_number = song_box.curselection()[0] + 1
    if next_number == song_box.size():
        next_number = 0  # If the cursor in the end of the list - jump to the start of the playlist
        next_one = song_box.get(next_number)
    else:
        next_one = song_box.get(next_number)

    # Load and play song
    pygame.mixer.music.load(next_one)
    pygame.mixer.music.play(loops=0)

    # Clear active bar in playlist listbox
    song_box.selection_clear(0, tkinter.END)

    # New song bar
    song_box.activate(next_number)

    # Set Active Bar to the next song
    song_box.selection_set(next_number, last=None)


# Pause selected song
def pause(is_paused) -> None:
    global paused
    paused = is_paused

    if paused:
        return
    # Pause the song
    pygame.mixer.music.pause()
    paused = True


# Create Playlist Box
song_box = tkinter.Listbox(root, bg="white", fg="black", width=60, selectbackground="gray", selectforeground="black")
song_box.pack(pady=20)

# Define player Control Button Images
back_btn_img = tkinter.PhotoImage(file='/home/oleh/Downloads/previous.png')
forward_btn_img = tkinter.PhotoImage(file='/home/oleh/Downloads/next.png')
play_btn_img = tkinter.PhotoImage(file='/home/oleh/Downloads/play.png')
pause_btn_img = tkinter.PhotoImage(file='/home/oleh/Downloads/pause.png')
stop_btn_img = tkinter.PhotoImage(file='/home/oleh/Downloads/stop.png')

# Create Player Control Frame
controls_frame = tkinter.Frame(root)
controls_frame.pack()

# Create Player Control Buttons
back_button = tkinter.Button(controls_frame, image=back_btn_img, borderwidth=0, command=previous_song)
forward_button = tkinter.Button(controls_frame, image=forward_btn_img, borderwidth=0, command=next_song)
play_button = tkinter.Button(controls_frame, image=play_btn_img, borderwidth=0, command=lambda: play(paused))
stop_button = tkinter.Button(controls_frame, image=stop_btn_img, borderwidth=0, command=stop)
pause_button = tkinter.Button(controls_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))

back_button.grid(row=0, column=0)
forward_button.grid(row=0, column=4)
play_button.grid(row=0, column=2)
stop_button.grid(row=0, column=1)
pause_button.grid(row=0, column=3)

# Create Menu
my_menu = tkinter.Menu(root)
root.config(menu=my_menu)

# Add song menu
add_song_menu = tkinter.Menu(my_menu)
my_menu.add_cascade(label="Add song", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song To Playlist", command=add_song)

# Add meny songs in playlist
add_song_menu.add_command(label="Add a few songs to Playlist", command=add_songs)

root.mainloop()

"""if __name__ == '__main__':
    pass"""

# TODO
# To fix the problem with forward and previous button for cursor selection
# Stages to see the bug: 1. Add a few songs, play the first, but hop with your cursor on the 3d song and click forward
# There should play 2 song, but 4th is playing instead.
# The problem occurs, because of the one entity for managing the queue and song selection
