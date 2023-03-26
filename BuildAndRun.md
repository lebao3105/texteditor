## Requirements
```
python 3.8+ with pip and its development codes
gettext (optional)
Microsoft Visual C++ (Windows)
GTK3 development files + pkgconfig and C/C++ compilers (Linux)
```

## Install dependencies
```bash
$ pip install attrdict3
$ pip install configparser darkdetect pillow packaging wxpython # This will take minutes!
```

## Clone this repo
```bash
$ git clone https://git[hub/lab].com/lebao3105/texteditor.git -b wip/wx textworker
$ cd textworker
```

## Run
1. Get submodules:
```bash
$ git submodule update --init --recursive
```

2. Install dependencies from Pypi:
```bash
$ pip install attrdict3
$ pip install -r requirements.txt
```

3. Run!:
```bash
$ [python] -m textworker [file]
```

## Build/install
1. With ```builder.py```:
```bash
$ [python] builder.py [options]
```

Options are:
* build - outputs will be created under the ```dist/``` folder.
* install - install the project
* maketrans - make translations, will copy the results into the source code folder
* clean - clean everything - FileExistsError will be ignored!

2. Run commands yourself
a. Build: ```[python] -m pip install build wheel && [python] -m build```
b. Install: ```[python] -m pip install .```
