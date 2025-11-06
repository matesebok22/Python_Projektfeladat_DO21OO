from tkinter import Tk
from ui import App

def main():
    root = Tk()
    root.minsize(500, 400)
    App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
