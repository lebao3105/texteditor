# This is a window that ask the user for setup the language.
# Will run for the first-run.
from tkinter import *
from tkinter import ttk
import miscs.init
import miscs.get_config
from tkinter.font import BOLD
import main

def setup():
    setup_win = Tk()
    miscs.init.initialize(setup_win, 1)
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
    self.text1 = Label(self, text=_("Welcome to your new application!"), font=("Helvetica", 12))
    self.text2 = Label(self, text=_("Press next to continue"), font=("Helvetica", 12))
    self.next_button = Button(self, text=_("Next"), command=lambda: next_button_clicked(self))
    self.header.place(relx=0.5, rely=0.1, anchor=CENTER)
    self.text1.place(relx=0.5, rely=0.2, anchor=CENTER)
    self.text2.place(relx=0.5, rely=0.3, anchor=CENTER)
    self.next_button.place(relx=0.5, rely=0.4, anchor=CENTER)
    run_theme(self)

def destroy(self):
    self.header.destroy()
    self.text1.destroy()
    self.text2.destroy()

def next_button_clicked(self):
    # Destroy other widgets, although it's not necessary.
    destroy(self)
    # Now create new items
    ## Texts
    self.header = Label(self, text=_("Apperance"), font=("Helvetica", 20))
    self.text1 = Label(self, text=_("Choose your color"), font=("Helvetica", 12))
    self.text2 = Label(self, text=_("Choose your theme"), font=("Helvetica", 12))
    ## Colors
    options = [
        _("Light"),
        _("Dark"),
        _("Colorful")
    ]

    sub_options = [
        _("Default"),
        _("Green"),
        _("Blue"),
        _("Red"),
    ]

    self.color_var = StringVar()
    self.color_var.set(options[0])

    self.sub_color_var = StringVar()
    self.sub_color_var.set(sub_options[0])

    ## Combo boxes
    self.color_menu = ttk.Combobox(self, textvariable=self.color_var, 
                                    values=options, state="readonly")
    self.color_menu.current(0)
    self.color_sub = ttk.Combobox(self, textvariable=self.sub_color_var,
                                    values=sub_options, state="disbled")
    self.color_sub.current(0)
    self.color_menu.bind("<<ComboboxSelected>>", lambda event: color_changed(self))
    self.color_sub.bind("<<ComboboxSelected>>", lambda event: color_changed(self))

    # Place all
    self.header.place(relx=0.5, rely=0.1, anchor=CENTER)
    self.text2.place(relx=0.5, rely=0.4, anchor=CENTER)
    self.color_menu.place(relx=0.5, rely=0.3, anchor=CENTER)
    self.text1.place(relx=0.5, rely=0.2, anchor=CENTER)
    self.color_sub.place(relx=0.5, rely=0.4, anchor=CENTER)
    self.next_button.place(relx=0.5, rely=0.5, anchor=CENTER)
    run_theme(self)

def color_changed(self):
    if self.color_var.get() == _("Dark"):
        self.color_sub.configure(state="readonly")
        miscs.get_config.change_config(self.sub_color_var.get())
    else:
        self.color_sub.configure(state="disabled")

def run_theme(self):
    miscs.get_config.set_windows_color(self)
    miscs.get_config.change_text_color(self.header)
    miscs.get_config.change_text_color(self.text1)
    miscs.get_config.change_text_color(self.text2)

if __name__ == "__main__":
    setup()
    #main.main_win()