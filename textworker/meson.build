installdir = join_paths(moduledir, 'textworker')
scalable_icondir = join_paths('hicolor', 'scalable', 'apps')
icon_installdir = join_paths(get_option('datadir'), 'icons', scalable_icondir)

defs_conf = configuration_data()
defs_conf.set('LOCALE_DIR', localedir)
defs_conf.set('ICON_DIR', icon_installdir)

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
    out = 'me.lebao3105.textworker.pyw'
else
    out = 'me.lebao3105.textworker'
endif

configure_file(
    input: 'me.lebao3105.textworker.in',
    output: out,
    configuration: run_conf,
    install: true,
    install_dir: get_option('bindir')
)

toplv_sources = [
    '__init__.py',
    '__main__.py',
    'generic.py',
    'main.py',
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
subdir('images')
subdir('ui')