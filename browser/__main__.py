import sys
import tkinter

from .url import URL
from .browser import Browser

if __name__ == "__main__":
    url = URL(sys.argv[1])
    browser = Browser()
    browser.load(url)
    tkinter.mainloop()
