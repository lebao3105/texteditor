# Initialize for this application
# Including language, and configurations.
from tkinter import END
from tkinter.messagebox import askyesno
from . import file_operations, constant

def check_is_saved(self):
    """Checks if the document is saved.
    TODO: Use this function with multiple tabs (save them all or not)."""
    if self.text_editor.get(1.0, END) != ("\n" or ""):
        for items in constant.UNSAVED:
            if self.notebook.tab(self.notebook.select(), "text") in items:
                if askyesno(self._("Notification"),
                    self._("There are unsaved files. Are you want to save them?")):
                    file_operations.save_file(self)
                    return True
                else: return False
    else:
        return True

def ask_quit(self):
    if check_is_saved(self):
        if askyesno(self._("Text editor"), 
                self._("Are you sure want to quit the application?")):
            self.destroy()
            #exit()
        else:
            pass
    else:
        self.destroy()
