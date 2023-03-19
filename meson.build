project(
    'textworker',
    version: '1.6.alpha2',
    meson_version: '>= 0.59.0',
    default_options: [
        'warning_level=2',
        'werror=false'
    ],
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
    error('Only Python 3.8 or higher is supported.')
endif

# Dirs
prefix = get_option('prefix')
localedir = join_paths(prefix, get_option('localedir'))
moduledir = join_paths(prefix, get_option('datadir'), meson.project_name())

subproject('libtextworker')
subdir('po')
subdir('textworker')

if target_machine.system() != 'windows'
    gnome = import('gnome')
    gnome.post_install(
        glib_compile_schemas: true,
        gtk_update_icon_cache: true,
        update_desktop_database: true
    )
endif

message('Note: Please make sure that you have dependencies installed before you build this project.')
message('Read https://github.com/lebao3105/texteditor/blob/main/BuildAndRun.md for more infomation.')
message('Note: Only Python 3.8+ is supported here.')