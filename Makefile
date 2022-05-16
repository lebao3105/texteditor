# Makefile to install text-editor on Linux and BSD
## For everyone:
## This is (the program) NOT built from GTK/QT, so
## install python3-tk(inter) package.
## Installation is admin-privileges required, so 
## use sudo to install.
## To see all targets, use make help.

.PHONY: install help uninstall

install: $(wildcard src/*.py src/*/*.py) $(wildcard po/base.pot po/*/*.po)
	mkdir -p /usr/local/share/texteditor
	@echo Generating translation files...
	for i in $$(ls -d po/*/); do msgfmt $${i%%/}/LC_MESSAGES/base -o $${i%%/}/LC_MESSAGES/base.mo ; done
	@echo Installing files...
	cp -r src/* po /usr/local/share/texteditor
	cp data/*.png /usr/local/share/texteditor/
	cp data/*-symbolic.svg /usr/share/icons/hicolor/symbolic/apps
	for i in $$(ls data/ | grep r.*svg ); do cp data/$${i%%/} /usr/share/icons/hicolor/scalable/apps ; done
	cp data/*.desktop /usr/share/applications
	gtk-update-icon-cache /usr/share/icons/hicolor
	echo "Installation complete."
	@echo Done.

uninstall:
	rm -rf /usr/local/texteditor
	rm -f /usr/local/share/applications/org.lebao3105.texteditor.desktop
	rm -f /usr/local/share/icons/hicolor/scalable/apps/org.lebao3105.texteditor*.svg
	gtk-update-icon-cache /usr/share/icons/hicolor
	@echo Done.

help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@echo "	install		Install the program"
	@echo "	uninstall	Uninstall the program"
	@echo "	help		Show this help"



