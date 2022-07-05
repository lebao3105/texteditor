import sys
import tabs
import mainwindow
from miscs import file_operations
from os.path import exists

if __name__ == '__main__':
    
    root = mainwindow.MainWindow()
    
    n = len(sys.argv)
    if (n-1 > 0):
        if exists(sys.argv[1]):
            file_operations.openfilename(root, sys.argv[1])
        for i in range(2,n):
            if exists(sys.argv[i]):
                tabs.add_tab(root)
                file_operations.openfilename(root, sys.argv[i])
    else:
        pass
    
    root.mainloop()
        
