from tkinter import Tk
from ui_SMM import App

def main():
    root = Tk()
    root.minsize(500, 400)
    App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
