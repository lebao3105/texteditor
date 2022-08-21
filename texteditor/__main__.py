import sys
import texteditor.tabs
import texteditor.mainwindow
from texteditor.miscs import file_operations
from os.path import isfile

if __name__ == '__main__':
    
    root = texteditor.mainwindow.MainWindow()
    n = len(sys.argv)
    if (n-1 > 0):
        if isfile(sys.argv[1]):
            file_operations.openfilename(root, sys.argv[1])
        for i in range(2,n):
            if isfile(sys.argv[i]):
                texteditor.tabs.add_tab(root)
                file_operations.openfilename(root, sys.argv[i])
    else:
        pass
    
    root.mainloop()        
