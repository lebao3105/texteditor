<<<<<<< HEAD
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
        
=======
import sys
import tabs
import mainwindow
from miscs import file_operations
from os.path import isfile

if __name__ == '__main__':
    
    root = mainwindow.MainWindow()
    
    n = len(sys.argv)
    if (n-1 > 0):
        if isfile(sys.argv[1]):
            file_operations.openfilename(root, sys.argv[1])
        for i in range(2,n):
            if isfile(sys.argv[i]):
                tabs.add_tab(root)
                file_operations.openfilename(root, sys.argv[i])
    else:
        pass
    
    root.mainloop()        
>>>>>>> b35a36977b88c3114d7f544fec4c57ce48b0658f
