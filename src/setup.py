# This is a window that ask the user for setup the language.
# Will run for the first-run.
from tkinter import *
from tkinter import ttk
import gettext
from tkinter.font import BOLD
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
    self.header = Label(self, text=_("Welcome"), font=("Helvetica", 20))
    self.text = Label(self, text=_("Welcome to your new application!"), font=("Helvetica", 12))
    self.text2 = Label(self, text=_("Press next to continue"), font=("Helvetica", 12))
    self.next_button = Button(self, text=_("Next"), command=lambda: next_button_clicked(self))
    self.header.place(relx=0.5, rely=0.1, anchor=CENTER)
    self.text.place(relx=0.5, rely=0.2, anchor=CENTER)
    self.text2.place(relx=0.5, rely=0.3, anchor=CENTER)
    self.next_button.place(relx=0.5, rely=0.4, anchor=CENTER)


def next_button_clicked(self):
    self.destroy()
    main.main()

if __name__ == "__main__":
    setup()
    #main.main_win()