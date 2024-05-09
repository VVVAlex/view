# pip install tkinterdnd2-universal

from tkinter import StringVar, TOP
from tkinterdnd2 import TkinterDnD, DND_ALL  # , DND_FILES
import customtkinter as ctk

class Tk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

ctk.set_appearance_mode("dark")
#ctk.set_default_color_theme("blue")

def get_path(event):
    pathLabel.configure(text = event.data)

#root = TkinterDnD.Tk()
root = Tk()
root.geometry("350x100")
root.title("Get file path")

nameVar = StringVar()

entryWidget = ctk.CTkEntry(root)
entryWidget.pack(side=TOP, padx=5, pady=5)

pathLabel = ctk.CTkLabel(root, text="Drag and drop file in the entry box")
pathLabel.pack(side=TOP)

entryWidget.drop_target_register(DND_ALL)           # DND_FILES
entryWidget.dnd_bind("<<Drop>>", get_path)

root.mainloop()
