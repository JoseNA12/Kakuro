from tkinter import *

class App:
    def __init__(self, master):
        self.display_button_entry(master)

    def setup_window(self, master):
        self.f = Frame(master, height=480, width=640, padx=10, pady=12)
        self.f.pack_propagate(0)

    def display_button_entry(self, master):
        self.setup_window(master)
        v = StringVar()
        self.e = Entry(self.f, textvariable=v)
        buttonA = Button(self.f, text="Cancel", command=self.cancelbutton)
        buttonB = Button(self.f, text="OK", command=self.okbutton)
        self.e.pack()
        buttonA.pack()
        buttonB.pack()
        self.f.pack()

    def cancelbutton(self):
        print (self.e.get())
        self.f.destroy()

    def okbutton(self):
        print (self.e.get())


def main():
    root = Tk()
    root.title('ButtonEntryCombo')
    root.resizable(width=NO, height=NO)
    app = App(root)
    root.mainloop()

main()