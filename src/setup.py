from tkinter import *
import main

def setup():
    setup_win = Tk()
    setup_win.title("Setup your language")
    setup_win.rowconfigure(0, weight=1)
    setup_win.columnconfigure(0, weight=1)
    place_setup_widgets(setup_win)
    setup_win.mainloop()

def place_setup_widgets(self):
    # Labels
    self.label_setup = Label(self, text="Setup your language")
    self.label_setup_text = Label(self, text="Please select your language")
    self.label_setup.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    self.label_setup_text.grid(row=1, column=0, sticky="ew", padx=5)

    # A dropdown menu
    options = [
        "English",
        "Vietnamese"
    ]

    self.clicked_option = StringVar()
    self.clicked_option.set("English")

    self.dropdown_menu = OptionMenu(self, self.clicked_option, *options)
    self.dropdown_menu.grid(row=2, column=0, sticky="ew", padx=5)

    # A button
    self.button_setup = Button(self, text="OK", command=lambda: language_checker(self))
    self.button_setup.grid(row=3, column=0, sticky="ew", padx=5)

def language_checker(self):
    if self.clicked_option.get() == "English":
        print("English option has been choosen.")
        main.language = "en"
    elif self.clicked_option.get() == "Vietnamese":
        print("Vietnamese choosed.")
        main.language = "vi"
    #print(main.language)
    self.destroy()

if __name__ == "__main__":
    setup()
    main.main_win()