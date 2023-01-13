import texteditor.backend
from tkinter import END, StringVar
from tkinter.ttk import Button, Entry, Frame, Label

texteditor.backend.require_version("1.6a", "<")

class Finder(Frame):
    def __init__(self, parent, option, event=None):
        if hasattr(parent, "findbox"):
            parent.findbox.destroy()
            parent.text_editor.tag_remove("found", 1.0, END)
        super().__init__()
        # Get some needed values
        self.text = parent.text_editor
        self.check_options(option)
        self.placewidgets()
        self.pack()
        parent.findbox = self

    def placewidgets(self):
        # Title first
        title = Label(self, text=_("Find something here..."))
        title.grid(row=0, column=0)
        # Find entry
        find_text = Label(self, text=_("Find"))
        find_text.grid(row=1, column=0)
        self.entry_find = Entry(self)
        self.entry_find.grid(row=1, column=1)
        # Start finding
        sv = StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv: self.search(sv.get()))
        self.entry_find.configure(textvariable=sv)

        # Replace
        if self.i == []:
            replace_text = Label(self, text=_("Replace"))
            replace_text.grid(row=2, column=0)
            self.entry_replace = Entry(self)
            self.entry_replace.grid(row=2, column=1)
            btn_replace = Button(self, text=_("Replace"))
            btn_replace.config(command=self.replace)
            btn_replace.grid(row=3, column=1)

        # Close widget
        quit = Button(self, text="Close")
        quit.grid(row=3, column=0)
        quit.config(command=self.destroy)

    def replace(self):
        while 1:
            self.rpl = self.entry_replace.get()
            if not self.rpl:
                break
            self.fnd = self.entry_find.get()
            self.textd = self.text.get(1.0, END)
            self.text.delete(1.0, END)
            self.text.insert(END, self.textd.replace(self.fnd, self.rpl))

    def search(self, find):
        pos = "1.0"
        self.text.tag_remove("found", pos, END)
        if find != "":
            while 1:
                pos = self.text.search(find, pos, nocase=1, stopindex=END)

                # Disabled because I've seen "Not found" label even there were highlighted texts
                # if not pos:
                #    self.searchfailed('create')
                #    break

                lastidx = "%s+%dc" % (pos, len(find))
                self.text.tag_add("found", pos, lastidx)
                pos = lastidx
            self.text.tag_config("found", background="yellow")

    def searchfailed(self, command: str):
        if command == "create":
            self.ia = Label(self, text="Not found", foreground="red")
            self.ia.grid(row=1, column=3)
        elif command == "destroy":
            if not hasattr(self.i, "Label"):
                return
            else:
                self.ia.destroy()

    def check_options(self, option):
        self.i = []
        self.i.clear()
        if option != "":
            self.i.append(option)
