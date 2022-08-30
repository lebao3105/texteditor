from . import __main__
import sys

def start():
    return __main__.start_app(sys.argv)

if __name__ == '__main__':
    start()