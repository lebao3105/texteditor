project('texteditor',
    version: '1.4-dev',
    meson_version: '>= 0.59.0',
    license: 'GPL-3.0+'
)

message('Note: Please make sure that you have Tkinter/Tk installed for your Python installation.')

# Import modules
i18n = import('i18n')
python = import('python')

# Check for the Python installation
py_inst = python.find_installation('python3')

if not py_inst.found()
    error('Python 3 installation not found!')
endif

if not py_inst.language_version().version_compare('>= 3.7')
    error('Only Python 3.7 and higher is supported.')
endif

subdir('po')
subdir('texteditor')