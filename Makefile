# Makefile to install text-editor on Linux and BSD,
# NOT compatible with Windows and macOS.
## For everyone:
## This is (the program) NOT built from GTK/QT, so
## install python3-tk(inter) package.
## Installation is admin-privileges required, so 
## use sudo to install.
## Installation is not required to run the program yet,
## and this is (the installation) still not working 
## properly. Now I lost ability to use gtk-update-icon-cache
## here, so I might use another Linux distribution.
## To see all targets, use make help.

.PHONY: install help uninstall

install: $(wildcard src/*.py src/*/*.py) $(wildcard po/base.pot po/*/*.po)
	mkdir -p /usr/share/texteditor
	@echo Generating translation files...
	for i in $$(ls -d po/*/); do msgfmt $${i%%/}/LC_MESSAGES/base -o $${i%%/}/LC_MESSAGES/base.mo ; done
	@echo Installing files...
	cp -r src/* po /usr/share/texteditor/
	cp data/*.png /usr/share/texteditor/
	mv /usr/share/texteditor/*.Devel.png /usr/share/texteditor/icon.png
	cp data/*-symbolic.svg /usr/share/icons/hicolor/symbolic/apps
	cp data/org.lebao3105.texteditor.Devel.svg /usr/share/icons/hicolor/scalable/apps
	cp data/*.desktop /usr/share/applications
	gtk-update-icon-cache /usr/share/icons/hicolor
	echo "Installation complete."
	@echo Done.

uninstall:
	rm -rf /usr/share/texteditor
	rm -f /usr/share/applications/org.lebao3105.texteditor.desktop
	rm -f /usr/share/icons/hicolor/scalable/apps/org.lebao3105.texteditor*.svg
	rm -f /usr/share/icons/hicolor/symbolic/apps/org.lebao3105.texteditor*.svg
	gtk-update-icon-cache /usr/share/icons/hicolor
	@echo Done.

help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@echo "	install		Install the program"
	@echo "	uninstall	Uninstall the program"
	@echo "	help		Show this help"
	@echo "Before install, make sure that you have:"
	@echo "	python3-tk	(or python-tk)"
	@echo "	python3		(or python-is-python3)"
	@echo "	python3-pip	(or python-pip) to install"
	@echo "             configparser package"
	@echo "If you have installed this application before,"
	@echo "Try to uninstall it first."



