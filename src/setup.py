# This is a window that ask the user for setup the language.
# Will run for the first-run.
from tkinter import *
from tkinter import ttk
import gettext
import main

_ = gettext.gettext

def setup():
    setup_win = Tk()
    setup_win.title(_("Setup your new application"))
    setup_win.resizable(False, False)
    setup_win.geometry("600x600")
    place_setup_widgets(setup_win)
    setup_win.mainloop()

# Therefore I'd like to ask the user to setup the language 
# before run the application, but now I think it's not necessary.
# I could check for Bottles's solution, but now let's make our new 
# world.
def place_setup_widgets(self):
    self.header = Label(self, text=_("Welcome"), font=("Arial", 20))
    self.header.grid(row=1, column=0, padx=10, pady=10)

if __name__ == "__main__":
    setup()
    main.main_win()