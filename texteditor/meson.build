installdir = join_paths(moduledir, 'texteditor')

defs_conf = configuration_data()
defs_conf.set('LOCALE_DIR', localedir)
defs_conf.set('VERSION', meson.project_version())

configure_file(
    input: 'defs.py.in',
    output: 'defs.py',
    configuration: defs_conf,
    install: true,
    install_dir: installdir
)

run_conf = configuration_data()
run_conf.set('PYTHON', py_inst.path())
run_conf.set('pkgdatadir', moduledir)

if target_machine.system() == 'windows'
    out = '@0@.pyw'.format(meson.project_name())
else
    out = '@0@'.format(meson.project_name())
endif

configure_file(
    input: '@0@.in'.format(meson.project_name()),
    output: out,
    configuration: run_conf,
    install: true,
    install_dir: get_option('bindir')
)

toplv_sources = [
    '__init__.py',
    '__main__.py',
    'mainwindow.py',
    'tabs.py'
]

install_data(
    toplv_sources,
    install_dir: installdir
)

subdir('backend')
subdir('extensions')
subdir('icons')
subdir('views')
