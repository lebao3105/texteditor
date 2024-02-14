# Used for maintaining tasks.
# Copyright (C) 2024 Le Bao Nguyen and contributors.
# Pround to be written in nano!

# Programs to use
UI2PY = wxformbuilder
GT = xgettext
MSF = msgfmt
MSM = msgmerge

# Project infomations
COPYRIGHT = "(C) 2024 Le Bao Nguyen and contributors."
PKGVER = "1.6b0" # Change this corresponding to the app version
UIFILES = $(wildcard textworker/ui/*.fbp)
LOCALES = vi # Language codes, separated using spaces
POFILES = # Make later

# Targets
.PHONY: genui maketrans makepot genmo $(UIFILES) $(LOCALES)

## Generate .py and .xrc
genui: $(UIFILES)

$(UIFILES):
	$(UI2PY) -g $@

## Generate translations
maketrans: makepot genmo

makepot: genui
	echo "[Translations] Making template..."
	$(GT) --copyright-holder=$(COPYRIGHT) --package-version=$(PKGVER) \
		--language=python -f po/POTFILES -d textworker -o po/textworker.pot

genmo: $(LOCALES)
$(LOCALES):
	echo "[Translations] Making po for $@..."
	$(MSM) po/$@.po po/textworker.pot -o po/$@.po

	echo "[Translations] Compiling po for $@..."

	if [ ! -d po/$@ ]; then \
		mkdir po/$@; \
	fi

	if [ ! -d po/$@/LC_MESSAGE ]; then \
		mkdir po/$@/LC_MESSAGE; \
	fi
	$(MSF) po/$@.po -o po/$@/LC_MESSAGE/$@.mo

install: maketrans
	$(pip) install .

build: maketrans
	$(pip) install build
	$(python3) -m build .

icons: $(wildcard textworker/data/icons/*.svg)
	rm textworker/icon.py
	touch textworker/icon.py
	$(img2py) -a -n dev $? textworker/icon.py

clean: $(wildcard po/*/LC_MESSAGES) $(wildcard textworker/ui/*.py)
	rm -rf $?
