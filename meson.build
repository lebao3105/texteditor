project(
    'texteditor',
    version: '1.4.0',
    meson_version: '>= 0.59.0',
    license: 'GPL-3.0+'
)

message('Note: Please make sure that you have dependencies installed before building this project.')
message('Note: Only Python3.7+ is supported here.')

# Import modules
i18n = import('i18n')
python = import('python')

# Check for the Python installation
py_inst = python.find_installation('python3')

if not py_inst.found()
    error('Python 3 installation not found!')
endif

if not py_inst.language_version().version_compare('>= 3.8')
    error('Only Python 3.8 and higher is supported.')
endif

prefix = get_option('prefix')
localedir = join_paths(prefix, get_option('localedir'))
moduledir = join_paths(prefix, get_option('datadir'), meson.project_name())

subdir('po')
subdir('texteditor')
