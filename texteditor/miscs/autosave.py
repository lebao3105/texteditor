from . import get_config
from tkinter.ttk import Combobox
from tkinter import Label, Toplevel, StringVar
import tkinter.messagebox

class AutoSave:
    """Contructs the autosaving files function on texteditor.\n
    Configurations:\n
    forceEnable : bool : Force enable this\n
    useTime : int : Force auto save after a time\n
    Function:\n
    openpopup : Make a popup window which asks the user to change the auto save time.
    It will change the useTime!\n
    """
    forceEnable : bool = False
    useTime : int = int(get_config.getvalue("filemgr", "autosave-time"))

    def __init__(self, master):
        super().__init__()
        
        self.autosave = get_config.getvalue("filemgr", "autosave")
        self.savetime = get_config.getvalue("filemgr", "autosave-time")
        self._do_check()
        self.parent = master

    def _do_check(self):
        if self.forceEnable == False:
            if self.autosave == 'yes':
                pass
            else:
                raise Exception ("Autosave is disabled on user configuration file")

        if self.useTime == int(self.savetime):
            print("Note: Autosave time used in AutoSave class = autosave-time in user configuration file")
            pass
        
        if (self.useTime or int(self.savetime)) > 30: # 30 minutes
            raise Exception ("Auto save time is higher than 30 minutes")
        
        if (self.useTime or int(self.savetime)) < 0.5: # 30 secs
            raise Exception ("Auto save time is smaller than 0.5 minute!")
    
    def openpopup(self):
        askwin = Toplevel(self.parent)
        askwin.geometry("350x200")
        askwin.resizable(False, False)
        selected_time = StringVar()
        label = Label(askwin, text="Select autosave time (minutes)\nAutosave function will be launched after a time.")
        cb = Combobox(askwin, textvariable=selected_time)
        cb['values'] = [0.5, 1, 2, 5, 10, 15, 20, 30]
        cb['state'] = 'readonly'
        label.pack(fill='x')
        cb.pack(fill='x', padx=15, pady=15)
        cb.bind('<<ComboboxSelected>>', lambda event: self.config(selected_time.get()))
        #get_config.set_window_color(askwin)
    
    def config(self, useTime, event=None):
        print(useTime)
        self.useTime = int(useTime)
        self._do_check()

"""import tkinter
root = tkinter.Tk()
class test(AutoSave):
    forceEnable = True
    useTime = 10

    def __init__(self, master):
        super().__init__(master)
        self.openpopup()
test(root)
root.mainloop()"""
