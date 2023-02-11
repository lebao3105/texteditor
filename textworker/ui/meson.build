ui_sources = [
    'preferences.xrc'
]
# Translation
run_command('pywxrc', '--gettext', 'preferences.xrc', '-o', '../../po/preferences.pot', check:true)

install_data(
    ui_sources,
    install_dir: join_paths(installdir, 'ui')
)