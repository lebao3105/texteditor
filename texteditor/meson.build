defs_conf = configuration_data()
defs_conf.set('LOCALE_DIR', localedir)
defs_conf.set('VERSION', meson.project_version())

configure_file(
    input: 'defs.py.in',
    output: 'defs.py',
    configuration: defs_conf,
    install_dir: moduledir
)

toplv_sources = [
    '__init__.py',
    '__main__.py',
    'mainwindow.py',
    'tabs.py'
]

install_data(
    toplv_sources,
    install_dir: moduledir
)

subdir('backend')
subdir('extensions')
subdir('icons')
subdir('views')
