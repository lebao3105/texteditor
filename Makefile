# Used for maintaining tasks.
# Copyright (C) 2024 Le Bao Nguyen and contributors.
# Pround to be written in nano!

# Programs to use
UI2PY = wxformbuilder
GT = xgettext
MSF = msgfmt
MSM = msgmerge

# Project infomations
FBPFILES = $(wildcard textworker/ui/*.fbp)
GENERATED_FILES = $(wildcard textworker/ui/*_generated.py)
LOCALES = vi # Language codes, separated using spaces
POFILES = # Make later
EMBEDIMG_WHERE = -d $(DATAPATH)
ifeq ($(DATAPATH),)
EMBEDIMG_WHERE =
endif

# Targets
.PHONY: all genui maketrans makepot genmo $(FBPFILES) $(LOCALES) build install icons splash assets

all: clean genui icons splash assets build

## Generate .py
genui: $(FBPFILES)

$(FBPFILES):
	$(UI2PY) -g $@

## Generate translations
maketrans: makepot genmo

makepot:
	@echo "[Translations] Making templates..."
	$(GT) --language=python -f po/POTFILES -d textworker -o po/textworker.pot

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
	$(python3) -m build


## Generate icons
icons:
	$(python3) embedimgs.py -t icons $(EMBEDIMG_WHERE)

## Generate splash screen (both light and dark mode)
splash:
	$(python3) embedimgs.py -t splash $(EMBEDIMG_WHERE)

## Generate assets (finally!)
assets:
	$(python3) embedimgs.py -t assets

## Clean
clean: $(wildcard po/*/LC_MESSAGES) $(wildcard textworker/ui/*_generated.py) $(wildcard data/*.png)
	rm -rf $?
