## Frequently asked questions

### General

1. Can't install wxPython

wxPython should have wheels for your OS + Python, if not:

Did you installed all dependencies first?

Also install attrdict3 before the wxPython installation.

Online forums may help.

2. Translations not correct/missing

You can make a GitHub issue [here.](https://github.com/lebao3105/texteditor/issues)

3. about.py / preferences.py / *.xrc: File not found

Those are wx's generated files, which must be **done** before the global publishment.

If you are running from source code: use wxFormBuilder to generate code from .fbp files in textworker/ui.

Using (py)wxrc does NOT work!

With wxFormBuilder installed and added to PATH (don't worry if you're on *NIX, they should do it for you), run:

```bash
$ wxformbuilder -g textworker/ui/(file).fbp
```

With ``(file)`` is the corresponding file name you need to use (about/preferences).

Or with make:

```bash
$ make genui
```

This step is required for updating translations.