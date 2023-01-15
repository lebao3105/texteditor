branch = get_option('branch')

if branch == 'stable'
    icon = ('@0@.svg').format(meson.project_name())
else
    icon = ('@0@.svg').format('me.lebao3105.textworker.Devel')
endif

install_data(
    join_paths('svg', icon),
    install_dir: icon_installdir
)
