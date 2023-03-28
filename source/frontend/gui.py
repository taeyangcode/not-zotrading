import tkinter as tk

class App(tk.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.root = master
        self._draw()

    def _draw(self):
        self.buttons = BuySell(self.root)
        self.buttons.pack(fill=tk.BOTH)

class BuySell(tk.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self._draw()
    
    def _draw(self):
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(fill=tk.BOTH)
        self.buy_button = tk.Button(self.button_frame, text="Buy")
        self.buy_button.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        self.sell_button = tk.Button(self.button_frame, text="Sell")
        self.sell_button.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)


if __name__ == "__main__":
    main = tk.Tk()
    main.geometry("720x480")
    myapp = App(main)
    myapp.mainloop()







