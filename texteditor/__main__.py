import sys
import texteditor.tabs
import texteditor.mainwindow
from texteditor.miscs import file_operations
from os.path import isfile

def start_app(argv:sys.argv):  
    root = texteditor.mainwindow.MainWindow()
    n = len(argv)
    if (n-1 > 0):
        if isfile(argv[1]):
            file_operations.openfilename(root, argv[1])
        for i in range(2,n):
            if isfile(argv[i]):
                texteditor.tabs.add_tab(root)
                file_operations.openfilename(root, argv[i])
    else:
        pass
    
    root.mainloop()

if __name__ == '__main__':
    sys.exit(start_app(sys.argv))