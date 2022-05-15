# Makefile to install text-editor on Linux and BSD
## For everyone:
## This is (the program) NOT built from GTK/QT, so
## install python3-tk(inter) package.
## Installation is admin-privileges required, so 
## use sudo to install.
## To see all targets, use make help.

.PHONY: install help uninstall
install: $(wildcard src/*.py src/*/*.py)
	mkdir -p /usr/local/texteditor
	cp -r src/* /usr/local/texteditor
	cp data/*.png /usr/local/share/icons/hicolor/
	cp data/*.svg /usr/local/share/icons/hicolor/
	cp data/*.desktop /usr/local/share/applications
	gtk-update-icon-cache /usr/local/share/icons/hicolor
	echo "Installation complete."
	@echo Done.

uninstall:
	rm -rf /usr/local/texteditor
	@echo Done.

help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@echo "	install		Install the program"
	@echo "	uninstall	Uninstall the program"
	@echo "	help		Show this help"



