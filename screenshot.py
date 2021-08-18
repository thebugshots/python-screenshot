import os, time
import tkinter as tk
from datetime import datetime
from functools import partial
from io import BytesIO
import win32clipboard
from PIL import Image
import pyscreenshot as ImageGrab

# Create folder snips if it doesn't exist
if not (os.path.isdir("snips")):
    os.mkdir("snips")

# Create Tkinter root
root = tk.Tk()
root.title("Screen Grabber")
favicon = tk.PhotoImage(file='assets/favicon.png')
root.iconphoto(False, favicon)

# Main canvas
canvas = tk.Canvas(root, width=500, height=250, bg="lightblue")

copy_clip = tk.IntVar()
show_clip = tk.IntVar()

copy_clip_check = tk.Checkbutton(root, text="Copy screenshot to clipboard", variable=copy_clip)
show_clip_check = tk.Checkbutton(root, text="Open screenshot after clip", variable=show_clip)

# Get dimensions from user
user_left = tk.Entry(root, text="0")
canvas.create_window(100, 45, window=user_left)
user_top = tk.Entry(root, text="100")
canvas.create_window(100, 75, window=user_top)
user_right = tk.Entry(root, text="500")
canvas.create_window(100, 105, window=user_right)
user_bottom = tk.Entry(root, text="400")
canvas.create_window(100, 135, window=user_bottom)

# Image copy status message
label = tk.Label(root, text="", bg="lightblue", font=('helvetica', 10))
canvas.create_window(250, 230, window=label)


def prepare_to_copy_clipboard(file_path):
    image = Image.open(file_path)
    output = BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()
    send_to_clipboard(win32clipboard.CF_DIB, data)


def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()


def clip_screen(dimensions):
    root.withdraw()
    time.sleep(0.3)
    image_name = "snips/" + str(datetime.now()).replace(" ", "").replace(":", "") + ".png"
    try:
        if dimensions:
            image = ImageGrab.grab(bbox=tuple(map(int, dimensions)))
        else:
            image = ImageGrab.grab()
        image.save(image_name)
        if copy_clip.get():
            prepare_to_copy_clipboard(image_name)

        if show_clip.get():
            image.show()

    except Exception as e:
        print(e)
        return e
    root.deiconify()
    return "Screenshot saved as " + image_name


def get_fullscreen():
    label.configure(text=clip_screen(None))


fs_clip_button = tk.Button(text='Clip Full Screen',
                           command=partial(get_fullscreen),
                           bg="#8e936d", fg="black",
                           padx=10,
                           font=("Sans Serif", 9))
canvas.create_window(350, 110, window=fs_clip_button)


def get_user_dimensions():
    left = user_left.get().strip()
    top = user_top.get().strip()
    right = user_right.get().strip()
    bottom = user_bottom.get().strip()
    label.configure(text=clip_screen((left, top, right, bottom)))


dim_clip_button = tk.Button(text='Clip with Dimensions',
                            command=partial(get_user_dimensions),
                            bg="#8e936d", fg="black",
                            padx=10,
                            font=("Sans Serif", 9))
canvas.create_window(100, 190, window=dim_clip_button)

copy_clip_check.pack()
show_clip_check.pack()
canvas.pack()
root.mainloop()
