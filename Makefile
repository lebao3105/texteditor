# Used for maintaining tasks.
# Copyright (C) 2024 Le Bao Nguyen and contributors.
# Pround to be written in nano!

# Programs to use
UI2PY = wxformbuilder
GT = xgettext
MSF = msgfmt
MSM = msgmerge
XRC2GT = pywxrc # Change it to wxrc if you want (not tested)

# Project infomations
UIFILES = $(wildcard textworker/ui/*.fbp)
XRCFILES = $(wildcard textworker/ui/*.xrc)
LOCALES = vi # Language codes, separated using spaces
POFILES = # Make later

# Targets
.PHONY: all genui maketrans makepot genmo $(UIFILES) $(LOCALES) build install icons splash assets

all: clean icons splash assets build

## Generate .py and .xrc
genui: $(UIFILES)

$(UIFILES):
	$(UI2PY) -g $@

## Generate translations
maketrans: makepot genmo

makepot: genui
	@echo "[Translations] Making templates..."
	$(GT) --language=python -f po/POTFILES -d textworker -o po/textworker.pot

$(XRCFILES):
	$(XRC2GT) -g $@ -o po/

genmo: $(LOCALES)
$(LOCALES):
	@echo "[Translations] Making po for $@..."
	$(MSM) po/$@.po po/textworker.pot -o po/$@.po

	@echo "[Translations] Compiling po for $@..."

	if [ ! -d po/$@ ]; then \
		mkdir po/$@; \
	fi

	if [ ! -d po/$@/LC_MESSAGE ]; then \
		mkdir po/$@/LC_MESSAGE; \
	fi
	$(MSF) po/$@.po -o po/$@/LC_MESSAGE/$@.mo

## Install
install: maketrans
	$(pip) install .

## Build
build: maketrans
	$(pip) install build
	$(python3) -m build .

## Generate icons
icons:
	$(python) embedimgs.py -t icons -d $(DATAPATH)

## Generate splash screen (both light and dark mode)
splash:
	$(python) embedimgs.py -t splash -d $(DATAPATH)

## Generate assets (finally!)
assets:
	$(python) embedimgs.py -t assets

## Clean
clean: $(wildcard po/*/LC_MESSAGES) textworker/ui/preferences.py $(wildcard data/*.png)
	rm -rf $?
