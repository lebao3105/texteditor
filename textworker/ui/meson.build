ui_sources = [
    'autosave.xrc',
    'preferences.xrc'
]
# Translation
run_command('pywxrc',
    '--gettext',
    'autosave.xrc',
    'preferences.xrc',
    '-o',
    '../../po/preferences.pot',
    check:true
)

install_data(
    ui_sources,
    install_dir: join_paths(installdir, 'ui')
)