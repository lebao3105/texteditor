project(
    'me.lebao3105.texteditor',
    version: '1.4.1',
    meson_version: '>= 0.59.0',
    license: 'GPL-3.0+'
)

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

# Dirs
prefix = get_option('prefix')
localedir = join_paths(prefix, get_option('localedir'))
moduledir = join_paths(prefix, get_option('datadir'), meson.project_name())

subdir('po')
subdir('texteditor')

if target_machine.system() != 'windows'
    gnome = import('gnome')
    gnome.post_install(
        glib_compile_schemas: true,
        gtk_update_icon_cache: true,
        update_desktop_database: true
    )
endif

message('Note: Please make sure that you have dependencies installed before building this project.')
message('Note: Only Python3.8+ is supported here.')